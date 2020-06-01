"""Main controller routines for the P65 assembler.

	When invoked as main, interprets its command line and goes from there.
	Otherwise, use run_all to interpret a file set."""

# Copyright 2002 Michael C. Martin.
# You may use, modify, and distribute this file under the BSD
# license: See LICENSE.txt for details.

from __future__ import nested_scopes
import sys
import Ophis.Frontend
import Ophis.IR
import Ophis.CorePragmas
import Ophis.OldPragmas
import Ophis.Passes
import Ophis.Errors as Err
import Ophis.Environment
import Ophis.CmdLine


def usage():
	"Prints a usage message and quits."
	print("Usage:")
	print("\tOphis [options] infile outfile")
	print("")
	print("Options:")
	print("\t-6510 Allow 6510 undocumented opcodes")
	print("\t-d Allow deprecated pragmas")
	print("\t-v n Set verbosity to n (0-4, 1=default)")
	sys.exit(1)

def run_all(infile, outfile):
	"Transforms the source infile to a binary outfile."
	Err.count = 0
	z = Ophis.Frontend.parse(infile)
	env = Ophis.Environment.Environment()

	m = Ophis.Passes.ExpandMacros()
	i = Ophis.Passes.InitLabels()
	l_basic = Ophis.Passes.UpdateLabels()
	l = Ophis.Passes.FixPoint("label update", [l_basic], lambda: l_basic.changed == 0)
	c = Ophis.Passes.Collapse()
	a = Ophis.Passes.Assembler()

	passes = []
	passes.append(Ophis.Passes.DefineMacros())
	passes.append(Ophis.Passes.FixPoint("macro expansion", [m], lambda: m.changed == 0))
	passes.append(Ophis.Passes.FixPoint("label initialization", [i], lambda: i.changed == 0))
	passes.extend([Ophis.Passes.CircularityCheck(), Ophis.Passes.CheckExprs(), Ophis.Passes.EasyModes()])
	passes.append(Ophis.Passes.FixPoint("instruction selection", [l, c], lambda: c.collapsed == 0))
	passes.extend([Ophis.Passes.NormalizeModes(), Ophis.Passes.UpdateLabels(), a])

	for p in passes: p.go(z, env)

	if Err.count == 0:
		try:
			output = open(outfile, 'wb')
			output.write(bytes(a.output))
			output.close()
		except IOError:
			print("Could not write to "+outfile)
	else:
		Err.report()

def run_ophis():
	infile = None
	outfile = None

	p65_compatibility_mode = 0
	undocumented_opcodes = 0

	reading_arg = 0

	for x in sys.argv[1:]:
		if reading_arg:
			try:
				Ophis.CmdLine.verbose = int(x)
				reading_arg = 0
			except ValueError:
				print("FATAL: Non-integer passed as argument to -v")
				usage()
		elif x[0] == '-':
			if x == '-v':
				reading_arg = 1
			elif x == '-6510':
				undocumented_opcodes = 1
			elif x == '-d':
				p65_compatibility_mode = 1
			else:
				print("FATAL: Unknown option "+x)
				usage()
		elif infile == None:
			infile = x
		elif outfile == None:
			outfile = x
		else:
			print("FATAL: Too many files specified")
			usage()

	if infile is None:
		print("FATAL: No files specified")
		usage()

	if outfile is None:
		print("FATAL: No output file specified")
		usage()

	Ophis.Frontend.pragma_modules.append(Ophis.CorePragmas)

	if p65_compatibility_mode:
		Ophis.Frontend.pragma_modules.append(Ophis.OldPragmas)

	if undocumented_opcodes:
		Ophis.Opcodes.opcodes.update(undocops)

	Ophis.CorePragmas.resetRequire()
	run_all(infile, outfile)

if __name__ == '__main__':
	run_ophis()
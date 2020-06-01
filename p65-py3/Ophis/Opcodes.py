"""6502 and 6510 opcodes

	Tables for the assembly of 6502 and 6510 instructions, mapping
	opcodes and addressing modes to binary instructions.  Includes
	the undocumented 6510 ops, as described in the VICE manuals."""

# Copyright 2002 Michael C. Martin.
# You may use, modify, and distribute this file under the BSD
# license: See LICENSE.txt for details.

# Names of addressing modes
modes = ["Implied",         #  0
	 "Immediate",       #  1
	 "Zero Page",       #  2
	 "Zero Page, X",    #  3
	 "Zero Page, Y",    #  4
	 "Absolute",        #  5
	 "Absolute, X",     #  6
	 "Absolute, Y",     #  7
	 "(Indirect)",      #  8
	 "(Indirect, X)",   #  9
	 "(Indirect), Y",   # 10
	 "Relative"]        # 11

# Lengths of the argument
lengths = [0, 1, 1, 1, 1, 2, 2, 2, 2, 1, 1, 1]

#                   IMPL  IMME   ZP   ZP-X  ZP-Y  ABS   ABSX  ABSY  IND   INDX  INDY  REL
opcodes =  { "adc":(None, 0x69, 0x65, 0x75, None, 0x6D, 0x7D, 0x79, None, 0x61, 0x71, None),
             "and":(None, 0x29, 0x25, 0x35, None, 0x2D, 0x3D, 0x39, None, 0x21, 0x31, None),
             "asl":(0x0A, None, 0x06, 0x16, None, 0x0E, 0x1E, None, None, None, None, None),
             "bcc":(None, None, None, None, None, None, None, None, None, None, None, 0x90),
             "bcs":(None, None, None, None, None, None, None, None, None, None, None, 0xB0),
             "beq":(None, None, None, None, None, None, None, None, None, None, None, 0xF0),
             "bit":(None, None, 0x24, None, None, 0x2C, None, None, None, None, None, None),
             "bmi":(None, None, None, None, None, None, None, None, None, None, None, 0x30),
             "bne":(None, None, None, None, None, None, None, None, None, None, None, 0xD0),
             "bpl":(None, None, None, None, None, None, None, None, None, None, None, 0x10),
             "brk":(0x00, None, None, None, None, None, None, None, None, None, None, None),
             "bvc":(None, None, None, None, None, None, None, None, None, None, None, 0x50),
             "bvs":(None, None, None, None, None, None, None, None, None, None, None, 0x70),
             "clc":(0x18, None, None, None, None, None, None, None, None, None, None, None),
             "cld":(0xD8, None, None, None, None, None, None, None, None, None, None, None),
             "cli":(0x58, None, None, None, None, None, None, None, None, None, None, None),
             "clv":(0xB8, None, None, None, None, None, None, None, None, None, None, None),
             "cmp":(None, 0xC9, 0xC5, 0xD5, None, 0xCD, 0xDD, 0xD9, None, 0xC1, 0xD1, None),
             "cpx":(None, 0xE0, 0xE4, None, None, 0xEC, None, None, None, None, None, None),
             "cpy":(None, 0xC0, 0xC4, None, None, 0xCC, None, None, None, None, None, None),
             "dec":(None, None, 0xC6, 0xD6, None, 0xCE, 0xDE, None, None, None, None, None),
             "dex":(0xCA, None, None, None, None, None, None, None, None, None, None, None),
             "dey":(0x88, None, None, None, None, None, None, None, None, None, None, None),
             "eor":(None, 0x49, 0x45, 0x55, None, 0x4D, 0x5D, 0x59, None, 0x41, 0x51, None),
             "inc":(None, None, 0xE6, 0xF6, None, 0xEE, 0xFE, None, None, None, None, None),
             "inx":(0xE8, None, None, None, None, None, None, None, None, None, None, None),
             "iny":(0xC8, None, None, None, None, None, None, None, None, None, None, None),
             "jmp":(None, None, None, None, None, 0x4C, None, None, 0x6C, None, None, None),
             "jsr":(None, None, None, None, None, 0x20, None, None, None, None, None, None),
             "lda":(None, 0xA9, 0xA5, 0xB5, None, 0xAD, 0xBD, 0xB9, None, 0xA1, 0xB1, None),
             "ldx":(None, 0xA2, 0xA6, None, 0xB6, 0xAE, None, 0xBE, None, None, None, None),
             "ldy":(None, 0xA0, 0xA4, 0xB4, None, 0xAC, 0xBC, None, None, None, None, None),
             "lsr":(0x4A, None, 0x46, 0x56, None, 0x4E, 0x5E, None, None, None, None, None),
             "nop":(0xEA, None, None, None, None, None, None, None, None, None, None, None),
             "ora":(None, 0x09, 0x05, 0x15, None, 0x0D, 0x1D, 0x19, None, 0x01, 0x11, None),
             "pha":(0x48, None, None, None, None, None, None, None, None, None, None, None),
             "php":(0x08, None, None, None, None, None, None, None, None, None, None, None),
             "pla":(0x68, None, None, None, None, None, None, None, None, None, None, None),
             "plp":(0x28, None, None, None, None, None, None, None, None, None, None, None),
             "rol":(0x2A, None, 0x26, 0x36, None, 0x2E, 0x3E, None, None, None, None, None),
             "ror":(0x6A, None, 0x66, 0x76, None, 0x6E, 0x7E, None, None, None, None, None),
             "rti":(0x40, None, None, None, None, None, None, None, None, None, None, None),
             "rts":(0x60, None, None, None, None, None, None, None, None, None, None, None),
             "sbc":(None, 0xE9, 0xE5, 0xF5, None, 0xED, 0xFD, 0xF9, None, 0xE1, 0xF1, None),
             "sec":(0x38, None, None, None, None, None, None, None, None, None, None, None),
             "sed":(0xF8, None, None, None, None, None, None, None, None, None, None, None),
             "sei":(0x78, None, None, None, None, None, None, None, None, None, None, None),
             "sta":(None, None, 0x85, 0x95, None, 0x8D, 0x9D, 0x99, None, 0x81, 0x91, None),
             "stx":(None, None, 0x86, None, 0x96, 0x8E, None, None, None, None, None, None),
             "sty":(None, None, 0x84, 0x94, None, 0x8C, None, None, None, None, None, None),
             "tax":(0xAA, None, None, None, None, None, None, None, None, None, None, None),
             "tay":(0xA8, None, None, None, None, None, None, None, None, None, None, None),
             "tsx":(0xBA, None, None, None, None, None, None, None, None, None, None, None),
             "txa":(0x8A, None, None, None, None, None, None, None, None, None, None, None),
             "txs":(0x9A, None, None, None, None, None, None, None, None, None, None, None),
             "tya":(0x98, None, None, None, None, None, None, None, None, None, None, None) }

undocops = { "anc":(None, 0x0B, None, None, None, None, None, None, None, None, None, None),
             "ane":(None, 0x8B, None, None, None, None, None, None, None, None, None, None),
             "arr":(None, 0x6B, None, None, None, None, None, None, None, None, None, None),
             "asr":(None, 0x4B, None, None, None, None, None, None, None, None, None, None),
             "dcp":(None, None, 0xC7, 0xD7, None, 0xCF, 0xDF, 0xDB, None, 0xC3, 0xD3, None),
             "isb":(None, None, 0xE7, 0xF7, None, 0xEF, 0xFF, 0xFB, None, 0xE3, 0xF3, None),
             "las":(None, None, None, None, None, None, None, 0xBB, None, None, None, None),
             "lax":(None, None, 0xA7, None, 0xB7, 0xAF, None, 0xBF, None, 0xA3, 0xB3, None),
             "lxa":(None, 0xAB, None, None, None, None, None, None, None, None, None, None),
             "rla":(None, None, 0x27, 0x37, None, 0x2F, 0x3F, 0x3B, None, 0x23, 0x33, None),
             "rra":(None, None, 0x67, 0x77, None, 0x6F, 0x7F, 0x7B, None, 0x63, 0x73, None),
             "sax":(None, None, 0x87, None, 0x97, 0x8F, None, None, None, 0x83, None, None),
             "sbx":(None, 0xCB, None, None, None, None, None, None, None, None, None, None),
             "sha":(None, None, None, None, None, None, None, 0x9F, None, None, 0x93, None),
             "shs":(None, None, None, None, None, None, None, 0x9B, None, None, None, None),
             "shx":(None, None, None, None, None, None, None, 0x7E, None, None, None, None),
             "slo":(None, None, 0x07, 0x17, None, 0x0F, 0x1F, 0x1B, None, 0x03, 0x13, None),
             "sre":(None, None, 0x47, 0x57, None, 0x4F, 0x5F, 0x5B, None, 0x43, 0x53, None)}


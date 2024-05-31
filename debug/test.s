	.text
	.file	"test.ll"
	.globl	maxRangeSquared                 # -- Begin function maxRangeSquared
	.p2align	4, 0x90
	.type	maxRangeSquared,@function
maxRangeSquared:                        # @maxRangeSquared
	.cfi_startproc
# %bb.0:                                # %maxRangeSquared_entry
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	pushq	%r14
	pushq	%rbx
	subq	$32, %rsp
	.cfi_offset %rbx, -32
	.cfi_offset %r14, -24
	movl	%edi, -24(%rbp)
	movl	%esi, -32(%rbp)
	movb	$104, -25(%rbp)
	movq	__str_1@GOTPCREL(%rip), %rdi
	movq	%rdi, -40(%rbp)
	callq	print_string@PLT
	movl	-24(%rbp), %edi
	movl	$2, %esi
	callq	power_int@PLT
	movl	%eax, -20(%rbp)
	movl	%eax, %edi
	callq	print_int@PLT
	.p2align	4, 0x90
.LBB0_1:                                # %maxRangeSquared_entry
                                        # =>This Inner Loop Header: Depth=1
	movl	-24(%rbp), %eax
	cmpl	-32(%rbp), %eax
	jg	.LBB0_4
# %bb.2:                                # %while_loop_entry_2
                                        #   in Loop: Header=BB0_1 Depth=1
	movl	-24(%rbp), %edi
	movl	$2, %esi
	callq	power_int@PLT
	movq	%rsp, %rbx
	leaq	-16(%rbx), %r14
	movq	%r14, %rsp
	movl	%eax, -16(%rbx)
	movl	%eax, %edi
	callq	print_int@PLT
	movl	-16(%rbx), %eax
	cmpl	-20(%rbp), %eax
	jle	.LBB0_1
# %bb.3:                                # %while_loop_entry_2.if
                                        #   in Loop: Header=BB0_1 Depth=1
	movl	(%r14), %eax
	movl	%eax, -20(%rbp)
	jmp	.LBB0_1
.LBB0_4:                                # %while_loop_otherwise_2
	movl	-20(%rbp), %edi
	callq	print_int@PLT
	movl	-20(%rbp), %eax
	leaq	-16(%rbp), %rsp
	popq	%rbx
	popq	%r14
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end0:
	.size	maxRangeSquared, .Lfunc_end0-maxRangeSquared
	.cfi_endproc
                                        # -- End function
	.globl	main                            # -- Begin function main
	.p2align	4, 0x90
	.type	main,@function
main:                                   # @main
	.cfi_startproc
# %bb.0:                                # %main_entry
	subq	$24, %rsp
	.cfi_def_cfa_offset 32
	movq	%rdi, 16(%rsp)
	movq	actual_min@GOTPCREL(%rip), %rax
	movl	(%rax), %edi
	movq	actual_max@GOTPCREL(%rip), %rax
	movl	(%rax), %esi
	callq	maxRangeSquared@PLT
	movl	%eax, 12(%rsp)
	movl	%eax, %edi
	callq	print_int@PLT
	addq	$24, %rsp
	.cfi_def_cfa_offset 8
	retq
.Lfunc_end1:
	.size	main, .Lfunc_end1-main
	.cfi_endproc
                                        # -- End function
	.type	actual_min,@object              # @actual_min
	.data
	.globl	actual_min
	.p2align	2
actual_min:
	.long	4294967287                      # 0xfffffff7
	.size	actual_min, 4

	.type	actual_max,@object              # @actual_max
	.globl	actual_max
	.p2align	2
actual_max:
	.long	9                               # 0x9
	.size	actual_max, 4

	.type	__str_1,@object                 # @__str_1
	.section	.rodata,"a",@progbits
	.globl	__str_1
__str_1:
	.asciz	"hoje"
	.size	__str_1, 5

	.section	".note.GNU-stack","",@progbits

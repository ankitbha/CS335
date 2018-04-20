# Generated Code 
.data
a:  .space 4
bh:  .space 4
alla:  .space 4
product:  .space None
nl:   .asciiz  "\n"

.text
.globl main

.ent main
main:
	li $s5, 15
	li $s2, 1
L3:
L5:
	sub $sp, $sp, 4
	sw $s2, 0($sp)
	sub $sp, $sp, 4
	sw $s5, 0($sp)
	addi $sp, $sp, -12
	sw $fp, -8($sp)
	sw $ra, -4($sp)
	move $fp, $sp
	addi $sp, $sp, -20
	jal product
	move $sp, $fp
	lw $fp, -8($sp)
	lw $ra, -4($sp)
	li $v0, 1
	move, $a0, $s5
	syscall
	add $s2, $s2, $zero
	addi $s2, $s2, 1
	move $s2, $s2
	sw $s5, _t4
	sw $s2, _t5
	j L3
L12:
	j exit
product:
	lw $s5, -16($fp)
	lw $s2, -12($fp)
	mul $t1, $s2, $s5
	mul $t4, $t1, $s7
	mul $t0, $t4, $s0
	sw $t0, 0($fp)
	jr $ra
exit:
	li $v0, 10
	syscall

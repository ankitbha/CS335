# Generated Code 
.data
.text
.globl main

.ent main
main:
	mul $t3, $t5, $t5
	mul $t1, $s4, $s2
	li $s7, 1
	mul $s7, $s7, $t1
	mul $s5, $s2, $t5
	mul $t8, $s7, $s5
	mul $s0, $t3, $t8
	move $a0, $s0
li $v0, 9
syscall
	add $s1, $s6, $t6
	sub $t0, $t6, $s6
	add $t2, $t9, $t5
	mul $s3, $s1, $t1
	mul $t7, $s3, $s5
	add $t4, $t7, $zero
	addi $t4, $t4, 0
	sw $t3, _t0
	lw $t3, _t12
	mul $t3, $t0, $s5
	sw $t9, f
	lw $t9, _t13
	add $t9, $t4, $t3
	sw $t2, _t8
	lw $t2, _t14
	sw $s7, _t2
	lw $s7, _t8
	add $t2, $t9, $s7
	sw $s1, _t6
	lw $s1, arr
	la $s1, arr
	sw $t5, a
	lw $t5, _temp
	la $t5, arr
	mul $t2, $t2, 4
	add $t5, $t5, $t2
	sw 10, 0($t5)
	sw $t8, _t4
	lw $t8, _t15
	add $t8, $s6, $t6
	sw $s5, _t3
	lw $s5, _t16
	sub $s5, $t6, $s6
	sw $s4, bh
	lw $s4, _t17
	sw $t5, _temp
	lw $t5, f
	sw $s1, arr
	lw $s1, a
	add $s4, $t5, $s1
	sw $t4, _t11
	lw $t4, _t18
	mul $t4, $t8, $t1
	sw $t9, _t13
	lw $t9, _t19
	sw $s1, a
	lw $s1, _t3
	mul $t9, $t4, $s1
	sw $s4, _t17
	lw $s4, _t20
	add $s4, $t9, $zero
	addi $s4, $s4, 0
	sw $t3, _t12
	lw $t3, _t21
	mul $t3, $s5, $s1
	sw $s1, _t3
	lw $s1, _t22
	add $s1, $s4, $t3
	sw $s3, _t9
	lw $s3, _t23
	sw $s1, _t22
	lw $s1, _t17
	add $s3, $s1, $s1
	sw $s5, _t16
	lw $s5, arr
	la $s5, arr
	sw $s1, _t17
	lw $s1, _t24
	add $s3, $s3, $s3
	add $s3, $s3, $s3
	add $s3, $s5,$s3
	lw $s1, $s3
	sw $s4, _t20
	lw $s4, ll
	move $s4, $s1
	sw $t9, _t19
	lw $t9, _t25
	mul $t9, $t6, $t5
	sw $t0, _t7
	lw $t0, _t26
	sw $s6, d
	lw $s6, a
	sub $t0, $s6, $t9
	sw $t4, _t18
	lw $t4, _t27
	sw $t7, _t10
	lw $t7, d
	sub $t4, $t0, $t7
	sw $s3, _t23
	lw $s3, l
	move $s3, $t4
	li $v0, 1
	move, $a0, $s3
	syscall
	li $v0, 1
	move, $a0, $s4
	syscall
	j exit
exit:
	li $v0, 10
	syscall

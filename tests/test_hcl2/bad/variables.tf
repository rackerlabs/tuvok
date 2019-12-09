output "foo" {
  description = "I am a valid output block, but in the wrong file!"
  value       = aws_iam_role.role1.name
}

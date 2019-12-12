output "foo" {
  description = "I am a valid output block!"
  value       = aws_iam_role.role1.name
}

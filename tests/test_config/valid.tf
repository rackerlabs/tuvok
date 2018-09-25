variable "foo" {
    description = "I am a valid variable block!"
    type = "string"
    default = ""
}

output "foo" {
  description = "I am a valid output block!"
  default     = "Output"
}

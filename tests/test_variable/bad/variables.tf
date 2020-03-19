# A variable with no description

variable "foo" {
  type    = "string"
}

variable "bar" {
  description = "A variable with no type."
}

variable "baz" {
  description = "A variable with a preset default."
  type        = "string"
  default     = ""
}

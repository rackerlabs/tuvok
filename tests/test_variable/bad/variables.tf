variable "foo" {
  type    = "string"
  default = "" # A variable with no description
}

variable "bar" {
  description = "A variable with no type."
  default     = ""
}

# tuvok: (T)he (U)nnamed (V)alidator, (OK)?

![Tuvok](docs/tuvok.png)

> *[Tuvok](https://en.wikipedia.org/wiki/Tuvok)* `/ˈtuːvɒk/` is a fictional character in the Star Trek media franchise. One of the main characters on the television series Star Trek: Voyager, Tuvok is a member of the fictional Vulcan species who serves as the ship's second officer, Chief of Security, and Chief Tactical Officer. In the Star Trek universe, Vulcans seek to operate by logic and reason, with as little emotion as possible.

Like the Vuclan Tuvok, this project is intended to apply logic and reason to enforce a given set of Terraform standards.

## Using the Dockerfile provided with this project

#### Building the image
```
$ docker build -t tuvok .
Sending build context to Docker daemon  417.8kB
Step 1/11 : FROM python:3-alpine
 ---> 408808fb1a9e
Step 2/11 : LABEL maintainer="Rackspace"
 ---> Using cache
 ---> 7ffba978ee28
<snip output>
Successfully built 55d574d9bb8c
Successfully tagged tuvok:latest
```

#### Confirming it works
```
$ docker run tuvok
$ docker run tuvok -c "tuvok -V"
INFO:tuvok:Scanning 0 files and executing checks
$ docker run tuvok -c "tuvok --version"
version 0.0.1
```

#### Mounting a local directory 'tests' of files to check
```
$ docker run -v $(pwd)/tests:/root/tests:ro tuvok -c "tuvok -V /root/tests/"
INFO:tuvok:Scanning 15 files and executing checks
ERROR:tuvok:github_module_ref-Modules sourced from GitHub should be pinned FAIL in /root/tests/test_module/module_git_missingref.tf:some_module
ERROR:tuvok:github_module_ref-Modules sourced from GitHub should be pinned FAIL in /root/tests/test_module/module_github_missingref.tf:some_module
WARNING:tuvok:output_description-Outputs should contain description FAIL in /root/tests/test_output/bad/outputs.tf:foo
ERROR:tuvok:FileLayoutCheck-Ensure variables and outputs are only in files of the same name FAIL in /root/tests/test_plugins/bad/outputs.tf:variable:foo was not found in a file named variables.tf
ERROR:tuvok:FileLayoutCheck-Ensure variables and outputs are only in files of the same name FAIL in /root/tests/test_plugins/bad/variables.tf:output:foo was not found in a file named outputs.tf
ERROR:tuvok:variable_description-Variables must contain description FAIL in /root/tests/test_variable/bad/variables.tf:foo
ERROR:tuvok:variable_type-Variables must contain type FAIL in /root/tests/test_variable/bad/variables.tf:bar
```

#### Running other commands
```
$ docker run tuvok "ls -la"
total 16
drwx------    1 root     root          4096 Nov 14 15:53 .
drwxr-xr-x    1 root     root          4096 Nov 14 15:56 ..
drwxr-xr-x    3 root     root          4096 Nov 14 15:53 .cache
drwx------    4 root     root          4096 Nov 14 15:53 .local
$ docker run local/tuvok:latest -c "cd /tuvok && pytest -q"
................. [100%]
17 passed in 9.61 seconds
```

### Custom configuration files

Tuvok supports custom configuration rules, allowing the creation of additional rules, or overriding the behavior of existing rules.  The tool will load and merge configurations from any explicitly provided configuration file, or from any file named `.tuvok.json` in a scanned directory.  Currently, only jq based checks can be included in the custom configuration.  An example custom configuration file can be found below:

```JSON
{
  "checks": {
    "my_custom_check": {
      "description": "My Custom Check description",
      "severity": "ERROR",
      "type": "jq",
      "jq": ".module[] | keys[] | select(match(\"[A-Z-]\"))",
      "prevent_override": false
    }
  },
  "ignore": ["variable_type"]
}
```

- `checks` - A mapping of jq based configuration checks.  Existing checks can be overridden, and additional checks can be added.  Each check should be given a unique name.  Each check has the following properties.  These properties are optional when overriding an existing check, and required for additional checks:
  - `description` - A basic description of the configuration check
  - `severity` - The severity level of the check.  Allowed values include `INFO`, `WARNING`, & `ERROR`
  - `type` - The type of the configuration check.  Allowed values include `jq`
  - `jq` - The jq query string that matches test failures. (I.E. the example check will match any module with a logical name that includes upper case letters or dashes.)
  - `prevent_override` - A boolean flag that prevents other custom configurations from modifying the check.
- `ignore` - A list of check names that should be skipped by the tool when evaluating a file.

*NOTE:* The generated json format of files changed with version 0.1.0 of the tool when HCL2 support was added.  If custom config reules were created prior to this version, JQ query strings should be tested and updated as necessary.

## How to propose new rules

Please see the [contributing guidelines](docs/CONTRIBUTING.md) for general information on contributing to this project. The process for proposing additional rules, modifying existing rules, or removing/deprecating rules will be followed like any other contribution.

## Versioning

We plan to follow [semantic versioning](http://semver.org) for this tool.

Specifically for rules builtin to this tool, we will interpret SemVer as follows:

- Breaking changes (major version): rules being moved from WARN to ERROR
- Feature additions (minor version): rules added at WARN
- Bug fixes (patch version): correcting false positives and false negatives

## Why build another tool?

To review existing tools, we used the following criteria/feature rubric:
- _Style and Linting_: Syntax checking, reading .tf files, reading Terraform plan files
- _Matching Syntax_: Golang/Python/etc rules, jq or regex syntax, others (JSON, YAML)
- _Matching Targets_: Attributes, Resources, Files, Order within a file
- _Functional_: Easy to distribute/portable, can emit warnings, can generate documentation, well-maintained
- _Other/Misc_: Requires additional tooling/code be written, easy to develop/popular language, supports CloudFormation too, will easily be adapted to HCL2

Some tools we reviewed, with our comments:
- [json2hcl](https://github.com/kvz/json2hcl) - would require additional tooling, but fairly portable
- [tfjson](https://github.com/palantir/tfjson) - operates specifically on plan files
- [tflint](https://github.com/wata727/tflint) - looking more at logic bugs in AWS provider arguments than style/lint
- [terraformtestinglib](https://github.com/schubergphilis/terraformtestinglib) - some novel features, very complex rule syntax
- [terraform-validator](https://github.com/ApplauseOSS/terraform-validator) - JSON + Regex rules, string/global matching
- [terraform_validate](https://github.com/elmundio87/terraform_validate) - required Python rules, more logic bug checking than linting

When writing our own tool, we wanted the following:

- Python project for easy contributions
- Convert HCL to JSON and validate JSON for future-proofing and CloudFormation cross-compatibility
- Rules could be text/data, add Python rule support later
- Allow pluggable rules to be stored in the same repository as Terraform configuration
- Allow YAML or JSON configuration files to override warn/error behavior of rules
- First-class Windows support
- Docker/HyperV/container builds, versioned with the tool
- Rules are versioned with the tool itself
- Ignore plan files for now, but consider later

## Future plans

- Python rule support
- Rules that may take arguments (e.g. `file_exists(main.tf)`)
- CloudFormation support
- Non-Terraform-specific rules (e.g. to support `tfenv` standards or enforce a file exists os.exists)
- Open sourcing this tool

See [issues](issues) list for specific features and ideas.

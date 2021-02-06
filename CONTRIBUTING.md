Contributions
-------------
Contributions to libvirt\_vmcfg are welcome and deeply appreciated!

We ask a few things of our contributors as a condition of contributing.

Code of Conduct
===============
Contributors must follow the [contributor covenant](CODE_OF_CONDUCT.md). Objectionable behaviour should be reported in an issue or to me at [elizabeth.jennifer.myers@gmail.com](mailto:elizabeth.jennifer.myers@gmail.com).

Reporting issues
================
The set of guidelines for reporting a bug or requesting a feature are slightly different:

### Reporting a bug
Please follow these guidelines when reporting bugs:
* **The title must clearly but concisely describe the problem.** A good description is something like "Unexpected KeyError exception raised when fooarg is not passed to libvirt\_vmcfg.foomod.barfunc." A bad example is "Exception raised from barfunc."
* **Describe what the problem is in as much detail as possible.** Descriptions like "The function `barfunc` causes ValueError to be raised" are not helpful.
* **Describe the desired behaviour.** Sometimes the behaviour that the function gives is expected, but may otherwise be incorrect or not meet expectations.
* **Explain what versions you know are affected.** The bug may have been fixed in newer versions.
* **If applicable, create an irreducible test case.** This means that you should submit the simplest possible example that shows the bug. Dumping a huge blob of your code onto us (or worse, just linking to a project) is unproductive and makes it difficult to debug the issue.
* **All examples should have their variables and functions in English.** Giving examples in other languages makes it more difficult to discover the problem or understand what you mean.

### Feature requests
Please follow these guidelines when requesting a feature:
* **The title should explain what you would like as clearly but concisely as possible.** A good description is something like "Add support for the Xen hypervisor." A bad description is something like "Support for other hypervisors."
* **Explain what you would like in as much detail as possible.** Descriptions like "add barfunc to foomod" tell us nothing about what you would like to implement.
* **Describe the semantics of the new feature.** Explain what you believe the function should do semantically. Something like "Make it possible to emit a valid libvirt VM XML description for Xen PV domains" is a good explanation.
* **Does this feature require a version bump?** If so, please explain. We follow [semantic versioning](https://semver.org/).
* **Try to write a pseudocode mockup that would use the feature in question.** This gives a clearer idea of what you would like.

### Pull requests
They should follow the above guidelines, with a few additions:
* **Document your changes.** New classes, functions, etc. should have a meaningful doc string.
* ~~**Create tests.**~~ We're not set up yet to do tests. When we are, submit tests, please.
* ~~**Create docs.**~~ We're not set up yet to do docs. When we are, submit docs, please.
* **Bump the version accordingly.** We follow [semantic versioning](https://semver.org/).
* **One subject per commit.** Giant mystery meat commits that involve tons of unrelated features and fixes are messy and make the history needlessly hard. Break them up.

### Change of license issues
It is common for CC0/public domain projects to receive requests to change to a different license. Issues that ask for a change of license will be closed and locked with no further comment or consideration to prevent unproductive discussion.

Style
=====
Please follow [PEP 8](https://www.python.org/dev/peps/pep-0008/).

Discussion on whether or not to adopt a line length above 79 characters is welcomed. For now, stick to the limit.

Code licensing
==============
Note that all contributions to the project must be declared CC0 as per the [license](LICENSE.txt). Do not contribute code you do not have the rights to. Doing so will result in a permanent ban on project participation and removal of all offending code.

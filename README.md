# Extract version from Git

This small script is made to extract the version information out of the tags of
the git repository. The output of the script can be used inside a shell script
or inside a Makefile. In this way, the version information is used without
changing the source or any other temporary file.

The tag must be either "major.minor_beta" or "major.minor". The fields 'major'
and 'minor' must be numbers. This version can have a prefix "v" or "V" or even
"r" or "R". If such a prefix is detected, it will be stripped.

The field 'beta' can consist of letters and digits. This field can be used as
"beta marker" (beta11) or as patch (p123) or build level (B123 or 4711).

The following tags will be recognized by the script:
* `v1.0` -- major=1 minor=0
* `V1.2` -- major=1 minor=2
* `r2.3` -- major=2 minor=3
* `1.1` -- major=1 minor=1
* `v1.1_beta2` -- major=1 minor=1 beta="beta2"

If no matching tag is found, the numerical fields of the version
are set to 0 and the strings are cleared (empty).


## Information provided by Git

We assume that the developer tags the released commit object. The format of
the tag is described above. Nevertheless, it is possible to call the
script even if there are new commits made after tagging. This is detected and
reported as counter. This counter represents the number of commits following
after the tagged commit.

This information is shown together with the short hash of the commit object. A
typical output of git could look like this:

~~~~
$ git describe --tags --always --dirty --long
v1.6-0-gb00c2de
~~~~

What we see is the version tag `v1.6` the *behind counter* `0` and the short
hash `gb00c2de` of the commit.


## Parameters

The script can be called with several parameters. This parameters allows to
change the amount and format of the displayed information. Call the script with
`--help` for a complete list of parameters.

The following options are important:

* `-a`, `--all`      -- show all values delimited by a colon. Use `cut` to parse the values in Makefiles.
* `-M`, `--major`    -- only show major number
* `-m`, `--minor`    -- only show minor number
* `-b`, `--beta`     -- only show beta / build string

Without options, all details are presented as string.

**Sample:** a project without *beta tag*
~~~~
$ git describe --tags --always --dirty --long
v1.6-0-gb00c2de
$ extract-version.py
1.6 (0:gb00c2de)
$ extract-version.py --all
1:6::0:gb00c2de
$ extract-version.py --major
1
$ extract-version.py --minor
6
~~~~

**Sample:** a project with *beta tag*
~~~~
$ git describe --tags --always --dirty --long
v1.6_beta3-0-gb00c2de
$ extract-version.py
1.6-beta3 (0:gb00c2de)
$ extract-version.py --all
1:6:beta3:0:gb00c2de
$ extract-version.py --major
1
$ extract-version.py --minor
6
$ extract-version.py --beta
beta3
~~~~

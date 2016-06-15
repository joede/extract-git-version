#!/usr/bin/python
#
# https://github.com/joede/extract-git-version
# Joerg Desch <github@jdesch.de>
# License: GPL v3.0
#
# Script to extract a version information out of the tags of the
# git repository. The tag must be either "major.minor_beta" or
# "major.minor". The fields 'major' and 'minor' must be numbers.
# The field 'beta' can consist of letters and digits. This field
# can be used as "beta marker" (beta11) or as patch (p123) or build
# level (B123 or 4711).
#
# If no matching tag is found, the numerical fields of the version
# are set to 0 and the strings are cleared (empty).

from os.path import dirname, isdir
from subprocess import CalledProcessError, check_output
from optparse import OptionParser
import re

verbose = False
beta_re = re.compile("[rvRV]?([0-9]+)\.([0-9]+)_([a-zA-Z0-9]+)-([0-9]+)-(.*)")
final_re = re.compile("[rvRV]?([0-9]+)\.([0-9]+)-([0-9]+)-(.*)")

def extract_version():
    major = 0
    minor = 0
    git_behind = 0
    git_ref = ""
    beta_tag = ""
    if isdir('.git'):
        # Get the version using "git describe".
        cmd = 'git describe --tags --always --dirty --long'
	if verbose:
	    print "info: call:",cmd
        try:
            #version = check_output(cmd.split()).decode().strip()[len(PREFIX):]
            version = check_output(cmd.split())
            if verbose:
                print "info: git returned",version
        except CalledProcessError:
            raise RuntimeError("error: can't get tags from git")
        m = beta_re.match(version)
        if m != None:
            major = m.group(1)
            minor = m.group(2)
            beta_tag = m.group(3)
            git_behind = m.group(4)
            git_ref = m.group(5)
        else:
            m = final_re.match(version)
            if m != None:
                major = m.group(1)
                minor = m.group(2)
                git_behind = m.group(3)
                git_ref = m.group(4)
                beta_tag = ""
    else:
        raise RuntimeError('no git root found!')

    return [major,minor,beta_tag,git_behind,git_ref]


def main():
    usage = "usage: %prog [options] arg"
    opt_parser = OptionParser(usage)
    opt_parser.add_option("-v", "--verbose", action="store_true", dest="verbose",
                           help="show more information")
    opt_parser.add_option("-a", "--all", action="store_true", dest="want_all",
                          default=False, help="show all values delimited by a colon")
    opt_parser.add_option("-M", "--major", action="store_true", dest="want_major",
                          default=False, help="only show major number")
    opt_parser.add_option("-m", "--minor", action="store_true", dest="want_minor",
                          default=False, help="only show minor number")
    opt_parser.add_option("-b", "--beta", action="store_true", dest="want_beta",
                          default=False, help="only show beta / build string")

    # parse the options and set the global verbose flag too
    (options, args) = opt_parser.parse_args()
    verbose = options.verbose

    # OK, let's do our job
    try:
	v = extract_version()
    except:
        print "fatal: something strange happened..."
        return 1

    # proudly present the results. ;-)
    if options.verbose:
        print "result of version query: ",v
    if options.want_all:
        # all values parsable delimited by a colon
        print "%s:%s:%s:%s:%s" % (v[0],v[1],v[2],v[3],v[4])
    elif options.want_major:
        print v[0]
    elif options.want_minor:
        print v[1]
    elif options.want_beta:
        print v[2]
    else:
        # as string
        version = "%s.%s" % (v[0],v[1])
        behind = "%s" % v[3]
        if v[2] != "":
            version = version + "-" + v[2]
        if v[4] != "":
            version = version + " (" + behind + ":" + v[4] + ")"
        print version
    return 0

if __name__ == '__main__':
    main()

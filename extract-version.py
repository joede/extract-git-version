#!/usr/bin/python
#
# https://github.com/joede/extract-git-version
# Joerg Desch <github@jdesch.de>
# License: GPL v3.0
#
# Script to extract a version information out of the tags of the
# git repository. The tag must be either "major.minor_beta", "major.minor",
# "major.minor.patch_beta" or "major.minor.patch".
# The fields 'major', 'minor' and 'patch' must be numbers.
# The field 'beta' can consist of letters and digits. This field
# can be used as "beta marker" (beta11) or build level (B123 or 4711).
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
beta_re3 = re.compile("[rvRV]?([0-9]+)\.([0-9]+)\.([0-9]+)_([a-zA-Z0-9]+)-([0-9]+)-(.*)")
final_re3 = re.compile("[rvRV]?([0-9]+)\.([0-9]+)\.([0-9]+)-([0-9]+)-(.*)")

def extract_version(curr_path):
    git_base = ".git"
    major = ""
    minor = ""
    patchlvl = ""
    git_behind = ""
    git_ref = ""
    beta_tag = ""
    if curr_path != "":
        git_base = curr_path + "/.git"

    if isdir(git_base):
        # Get the version using "git describe".
        if curr_path != "":
            cmd = "git -C " + curr_path + " describe --tags --always --dirty --long"
        else:
            cmd = "git describe --tags --always --dirty --long"
        if verbose:
            print "info: call:",cmd
        try:
            #version = check_output(cmd.split()).decode().strip()[len(PREFIX):]
            version = check_output(cmd.split())
            if verbose:
                print "info: git returned",version
        except CalledProcessError:
            raise RuntimeError("error: can't get tags from git")
        m = beta_re3.match(version)
        if m != None:
            major = m.group(1)
            minor = m.group(2)
            patchlvl = m.group(3)
            beta_tag = m.group(4)
            git_behind = m.group(5)
            git_ref = m.group(6)
        else:
            m = final_re3.match(version)
            if m != None:
                major = m.group(1)
                minor = m.group(2)
                patchlvl = m.group(3)
                git_behind = m.group(4)
                git_ref = m.group(5)
            else:
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
    else:
        if verbose and (curr_path!=""):
            print "info: used working dir:",git_base
        raise RuntimeError('no git root found!')

    return [major,minor,patchlvl,beta_tag,git_behind,git_ref]


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
    opt_parser.add_option("-p", "--patchlevel", action="store_true", dest="want_patchlevel",
                          default=False, help="only show patchlevel number")
    opt_parser.add_option("-b", "--beta", action="store_true", dest="want_beta",
                          default=False, help="only show beta / build string")
    opt_parser.add_option("-C", "--current", dest="curr_path",
                          default="", help="path to current working directoy (with .git directory).")

    # parse the options and set the global verbose flag too
    (options, args) = opt_parser.parse_args()
    verbose = options.verbose

    # OK, let's do our job
    try:
	v = extract_version(options.curr_path)
    except:
        print "fatal: something strange happened..."
        return 1

    # proudly present the results. ;-)
    if options.verbose:
        print "result of version query: ",v
    if options.want_all:
        # all values parsable delimited by a colon
        print "%s:%s:%s:%s:%s:%s" % (v[0],v[1],v[2],v[3],v[4],v[5])
    elif options.want_major:
        print v[0]
    elif options.want_minor:
        print v[1]
    elif options.want_patchlevel:
        print v[2]
    elif options.want_beta:
        print v[3]
    else:
        # version as string, two or three parted
        if v[2] != "":
            version = "%s.%s.%s" % (v[0],v[1],v[2])
        else:
            version = "%s.%s" % (v[0],v[1])
        # append the optional beta tag
        if v[3] != "":
            version = version + "-" + v[3]
        # append optional commit reference
        behind = "%s" % v[4]
        if v[5] != "":
            version = version + " (" + behind + ":" + v[5] + ")"
        print version
    return 0

if __name__ == '__main__':
    main()

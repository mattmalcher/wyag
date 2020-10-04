## Note - had to set up smart indent for vim for this to be less painful http://henry.precheur.org/vim/python

# for handling command line args
import argparse

# for ordered dicts ... does python now have these?
import collections

#read and write config files (like .ini files)
import configparser

# gives us hashing functions
import hashlib

# for file handling
import os

# regular expressions (for excludes?)
import re

# to get at command line args
import sys

# for compression
import zlib

# Argument Parsing
# https://docs.python.org/3/library/argparse.html
argparser = argparse.ArgumentParser(description = "matts git")

# subparsers are the parsers for the second level command - i.e. (git) commit, (git) add etc
argsubparsers = argparser.add_subparsers(title="Commands", dest="command")
argsubparsers.required = True


# define a main function which takes the arguments provided to the executable and parses them then dispatches to one
# of the second level functions
def main(argv=sys.argv[1:]):
    args = argparser.parse_args(argv)

    if args.command == "add"         : cmd_add(args)
    elif args.command == "cat-file"    : cmd_cat_file(args)
    elif args.command == "checkout"    : cmd_checkout(args)
    elif args.command == "commit"      : cmd_commit(args)
    elif args.command == "hash-object" : cmd_hash_object(args)
    elif args.command == "init"        : cmd_init(args)
    elif args.command == "log"         : cmd_log(args)
    elif args.command == "ls-tree"     : cmd_ls_tree(args)
    elif args.command == "merge"       : cmd_merge(args)
    elif args.command == "rebase"      : cmd_rebase(args)
    elif args.command == "rev-parse"   : cmd_rev_parse(args)
    elif args.command == "rm"          : cmd_rm(args)
    elif args.command == "show-ref"    : cmd_show_ref(args)
    elif args.command == "tag"         : cmd_tag(args)


# Define a class for repositories and implement a few checks
# repo has a .git dir
# repo has a config file
# config file is of a version we can handle
# inherit from object class
class GitRepository(object):
    """A git repo"""

    worktree = None
    gitdir = None
    conf = None

    def __init__(self, path, force=False):

        self.worktree = path
        self.gitdir = os.path.join(path, ".git")

        if not (force or os.path.isdir(self.gitdir)):
            raise Exception("Not a Git repository silly! %s" % path)

        # read config file in .git/config
        self.conf = configparser.ConfigParser()
        cf = repo_file(self, "config")

        if cf and os.path.exists(cf):
            self.conf.read([cf])

        elif not force:
            raise Exception("Configuration file missing")

        if not force:
            vers = int(self.conf.get("core", "repositoryformatversion"))
            if vers != 0:
                raise Exception("Unsupported repositoryformatversion %s" % vers)


# Path building function
# n.b. the * indicates that an arg is a tuple (** = dict)
def repo_path(repo, *path):
    """ Comput path under repo's gitdir"""
    return os.path.join(repo.gitdir, *path)


# make path / file creating functions
def repo_file(repo, *path, mkdir=False):
    """Same as repo_path, but create dirname(*path) if absent.  For
    example, repo_file(r, \"refs\", \"remotes\", \"origin\", \"HEAD\") will create
    .git/refs/remotes/origin."""

    # slicing here takes the last element of path off (i.e. leaving directory)
    if repo_dir(repo, *path[:-1], mkdir=mkdir):
        return (repo_path(repo, *path))


def repo_dir(repo, *path, mkdir=False):
    """Same as repo_path, but mkdir *path if absent if mkdir."""

    path = repo_path(repo, *path)

    if os.path.exists(path):
        if (os.path.isdir(path)):
            return (path)
        else:
            raise Exception("Not a directory %s" % path)

    if mkdir:
        os.makedirs(path)
        return path
    else:
        return None


# Define how to create a repo
def repo_create(path):
    """Create a new repository at path."""
    # this is calling the __init__ method and saying force == True
    # this is because the checks would fail because the repo doesnt exist yet!
    repo = GitRepository(path, True)

    # check the path doesnt exist, or is an empty directory

    if os.path.exists(repo.worktree):
        if not os.path.isdir(repo.worktree):
            raise Exception("%s is not a directory!" % path)
        if os.listdir(repo.worktree):
            raise Exception("%s is not empty!" % path)

    else:
        os.makedirs(repo.worktree)

    # assert - i.e. ensure these return true (i.e. make these folders or die trying)
    assert (repo_dir(repo, "branches", mkdir=True))
    assert (repo_dir(repo, "objects", mkdir=True))
    assert (repo_dir(repo, "refs", "tags", mkdir=True))
    assert (repo_dir(repo, "refs", "heads", mkdir=True))

    # .git/description
    with open(repo_file(repo, "description"), "w") as f:
        f.write("Unnamed repository; edit this file 'description' to name the repository.\n")

    # .git/HEAD
    with open(repo_file(repo, "HEAD"), "w") as f:
        f.write("ref: refs/heads/master\n")

    with open(repo_file(repo, "config"), "w") as f:
        config = repo_default_config()  # see below
        config.write(f)

    return repo


# this function returns the default configuration for repositories
# filemode=false  means it ignores the permissions bist
# bare =false indicates the repo has a worktree (i.e. its not elsewher) not supported for this to be true
def repo_default_config():
    ret = configparser.ConfigParser()

    ret.add_section("core")
    ret.set("core", "repositoryformatversion", "0")
    ret.set("core", "filemode", "false")
    ret.set("core", "bare", "false")

    return ret


# Make command line interface
argsp = argsubparsers.add_parser("init", help="Initialize a new, empty repository.")

# add metadata about the arg which provides help/default values
argsp.add_argument("path",
                   metavar="directory",
                   nargs="?",
                   default=".",
                   help="Where to create the repository.")


# define the cmd_init function (as called by the top level dispatch) which then in turn calls repo_create
def cmd_init(args):
    repo_create(args.path)


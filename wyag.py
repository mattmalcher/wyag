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

###  Argument Parsing
# https://docs.python.org/3/library/argparse.html
argparser = argparse.ArgumentParser(description = "matts git")

# subparsers are the parsers for the second level command - i.e. (git) commmit, (git) add etc
argsubparsers = argparser.add_subparsers(title = "Commands", dest = "command")
argsubparsers.required = True

# define a main function which takes the arguments provided to the executable and parses them then dispatches to one of the second level functions
def main(argv=sys.argv[1:]):
    args = argparser.parse_args(argv)

    if   args.command == "add"         : cmd_add(args)
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



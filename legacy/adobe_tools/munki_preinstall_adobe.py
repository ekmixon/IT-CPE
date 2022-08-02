#!/usr/bin/python
# Copyright (c) Facebook, Inc. and its affiliates.
"""Check to see whether an Adobe entitlement has been added to the user."""

from __future__ import print_function
import sys

import adobe_tools

target_product = sys.argv[1]

me = ldap_lookup()  # Replace this with your own user lookup method
email = me.email
firstname = me.first_name
lastname = me.last_name
country = 'US'


def log(message):
  """Log with tag."""
  tag = 'CPE-check_adobe'
  print(tag + f': {str(message)}')


if email is None or email == '':
    # No user, could likely be root
  print(f"No email found for {me.username}")
  exit(0)

# Do I exist as a user?
user_exists = False
try:
  user_exists = adobe_tools.user_exists(email)
except Exception as e:
  log(f"EXCEPTION: {e}")
  # If any exceptions are generated, should assume not entitled
  exit(0)

if not user_exists:
    # User has no account, so obviously this isn't entitled
  log(f"User {email} does not have an existing account.")
  exit(0)

# Does the user already have the product?
log(f"Checking to see if {email} already has {target_product}")
already_have = False
try:
  already_have = adobe_tools.does_user_have_product(target_product, email)
except Exception as e:
  log(f"EXCEPTION: {e}")
  # If any exceptions are generated, should assume not entitled
  exit(0)

if already_have:
  log(f"User {email} already has product {target_product}")
  exit(1)

log(f"Eligible to install {target_product}.")

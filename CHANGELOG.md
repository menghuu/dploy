# Change Log

The format of this change log is based on [Keep a Changelog](http://keepachangelog.com/)

All changes documented here should be written with the goal give the end-user
(not other developers) a summarized view of the changes since the last release,
organized by order of importance.

## [Unreleased]
### Added
- Added optional is_silent & is_dry_run arguments to dploy.stow() dploy.unstow()
  and dploy.link(), This is analogous to the --dry-run and --quiet command line
  arguments. These function arguments default to is_silent=True and
  is_dry_run=False.
- Added --ignore argument to stow and unstow commands, to specify patterns file
  to ignore.
- Added reading of .dploystowignore files in the directories of sources for
  ignore patterns that are additional to those specified via --ignore
- Check for additional issues with sub commands that are similar to the initial
  checks done on the input of stow and unstow
- Check for source and dest new consideration was taken for sources
  and dests directories that have invalid execute permissions.
- Added redundant check to make sure dploy never deletes anything other than a
  symbolic link
### Changed
- Changed the output of failing dploy sub commands so they print as many
  detected issues as possible before aborting
- Print all conflicts while stowing instead of just the first conflict, and
  print what exactly the conflict is
- Display the user inputted source and dest paths instead of absolute paths in
  the output
- Clarify error messages for file and symbolic link conflicts
- Make the output of dploy stow and unstow deterministic across file systems
- Prevent redundant errors when the src or dest are not directories
- Clarify some error messages
### Fixed
- Fixed issue when unstowing where some stowed packages directories created
  during the stowing process via unfolding would not be deleted.
### Removed
-

## [0.0.3]
### Added
- Adds support for python 3.3
- Add an unstow command to undo stowing
### Changed
- Stow command is run in two passes and check for conflicts first before making
  any changes
### Fixed
- General bug fixes and improvements.

#!/bin/sh

# Usage: ./make-git-snapshot.sh [COMMIT]
#
# to make a snapshot of the given tag/branch.  Defaults to HEAD.
# Point env var REF to a local mesa repo to reduce clone time.

VERSION="11.2"
DIRNAME=mesa-${VERSION}-$( date +%Y%m%d )

if [ -z "$REF" -a -d "mesa/.git" ]; then
	  REF="mesa"
  fi

  echo REF ${REF:+--reference $REF}
  echo DIRNAME $DIRNAME
  echo HEAD ${1:-HEAD}

  rm -rf $DIRNAME

  git clone ${REF:+--reference $REF} \
	  	git://git.freedesktop.org/git/mesa/mesa $DIRNAME

  GIT_DIR=$DIRNAME/.git git archive --format=tar --prefix=$DIRNAME/ ${1:-HEAD} \
		| xz -vf > $DIRNAME.tar.xz

  # rm -rf $DIRNAME

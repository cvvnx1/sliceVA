#!/bin/echo - This is a function source file

# Usage method:
# . function.sh

#################################
# _replace_str()
#
# used for replace string from old string to new string in a file
#
# Usage method:
# _replace_str $old_str $new_str $file_path
#
#################################
_replace_str(){
  if [ -w $3 ]; then
    sed -i "s/${1}/${2}/g" $3
  else
    echo "$3 can not modify in _replace_str!"
    exit 1
  fi
}

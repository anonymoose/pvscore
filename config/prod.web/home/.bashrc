# .bashrc

# Source global definitions
if [ -f /etc/bashrc ]; then
	. /etc/bashrc
fi

# User specific aliases and functions

# .bashrc

# Source global definitions
if [ -f /etc/bashrc ]; then
	. /etc/bashrc
fi

# User specific aliases and functions
export HISTFILESIZE=1000000000
export HISTSIZE=1000000
export HISTCONTROL=ignoredups 
PATH=$PATH:.:/usr/pgsql-9.1/bin
export PATH
alias ll="ls -aGFlh"
alias ...="cd ../.."
alias la='ls -Al'               # show hidden files
alias ls='ls -aF' # add colors and file type extensions
alias lx='ls -lXB'              # sort by extension
alias lk='ls -lSr'              # sort by size
alias lc='ls -lcr'      # sort by change time
alias lu='ls -lur'      # sort by access time
alias lr='ls -lR'               # recursive ls
alias lt='ls -ltr'              # sort by date
alias lm='ls -al |more'         # pipe through 'more'


export LD_LIBRARY_PATH=/usr/pgsql-9.1/lib:$LD_LIBRARY_PATH


#!/bin/bash
module load savu/1.2
module load global/cluster-quiet

# function for parsing optional arguments
function arg_parse ()
{
  flag=$1
  return=$2
  while [[ $# -gt 3 ]] ; do
    if [ $3 == $flag ] ; then
      eval "$return"=$4
    fi
    shift
  done
}

if [[ $@ == '--help' ]] ; then
    echo -e "\n\t************************* SAVU HELP MESSAGE ****************************"
    tput setaf 6
    echo -e "\n\t To submit a Savu parallel job to the cluster, please follow the "
    echo -e "\t template below:"
    tput sgr0
    echo -e "\n\t >>> savu_mpi  <in_file>  <process_list>  <out_folder>  <optional_args>"
    tput setaf 6
    echo -e "\n\t For a list of optional arguments type:"
    tput sgr0
    echo -e "\t >>> savu --help"
    tput setaf 6
    echo -e "\n\t It is recommended that you pass the optional arg '-d <temp_dir>', "
    echo -e "\t where temp_dir is the temporary directory for your visit, if you are "
    echo -e "\t running Savu on a full dataset. Ask your local contact for help."
    tput sgr0
    echo -e "\n\t\t\t *** THANK YOU FOR USING SAVU! ***"
    echo -e "\n\t************************************************************************\n"
    tput sgr0
    exit    
fi

# Check required arguments exist
vars=$@
x="${vars%%' -'*}"
[[ $x = $vars ]] && temp=${#vars} || temp=${#x}
args=(${vars:0:$temp})
nargs=${#args[@]}

if [ $nargs != 3 ] ; then
    tput setaf 1    
    echo -e "\n\t************************* SAVU INPUT ERROR *****************************"
    tput setaf 6
    echo -e "\n\t You have entered an incorrect number of input arguments.  Please follow"
    echo -e "\t the template below:"
    tput sgr0
    echo -e "\n\t >>> savu_mpi  <in_file>  <process_list>  <out_folder>  <optional_args>"
    tput setaf 6
    echo -e "\n\t For a list of optional arguments type:"
    tput sgr0
    echo -e "\t >>> savu --help"
#    tput setaf 6
    echo -e "\n\t\t\t *** THANK YOU FOR USING SAVU! ***"
    tput setaf 1
    echo -e "\n\t************************************************************************\n"
    tput sgr0
    exit
fi

# set parameters
datafile=$1
processfile=$2
outpath=$3
shift 3
options=$@

outname=savu
nNodes=2
nCoresPerNode=20
nGPUs=4

# get the Savu path
DIR="$(cd "$(dirname "$0")" && pwd)"
filepath=$DIR'/savu_mpijob.sh'
savupath=$(python -c "import savu, os; print savu.__path__[0]")
savupath=${savupath%/savu}

echo -e "\t The Savu path is:" $savupath

M=$((nNodes*nCoresPerNode))

# set the output folder
arg_parse "-f" foldername "$@"
if [ ! $foldername ] ; then
  IFS=. read path ext <<<"${datafile##*-}"
  foldername=$(date +%Y%m%d%H%M%S)"_$(basename $path)"
fi
outfolder=$outpath/$foldername
# check the output folder exists - error if not

# create the output folder
if [ ! -d $outfolder ]; then
  echo -e "\t Creating the output folder "$outfolder
  mkdir -p $outfolder;
fi
# create the user log
touch $outfolder/user.log

# set the intermediate folder
arg_parse "-d" interfolder "$@"
if [ ! $interfolder ] ; then
  interfolder=$outfolder
fi

qsub -jsv /dls_sw/apps/sge/common/JSVs/tomo_recon_test.pl \
     -N $outname -j y -o $interfolder -e $interfolder -pe openmpi $M -l exclusive \
     -l infiniband -l gpu=4 -l gpu_arch=Kepler $filepath $savupath $datafile \
     $processfile $outpath $nCoresPerNode $nGPUs $options -c \
     -f $outfolder -s cs04r-sc-serv-14 -l $outfolder > /dls/tmp/savu/$USER.out


# get the job number here
filename=`echo $outname.o`
jobnumber=`awk '{print $3}' /dls/tmp/savu/$USER.out | head -n 1`

echo -e "\n\t************************************************************************"
echo -e "\n\t\t\t *** THANK YOU FOR USING SAVU! ***"
tput setaf 6
echo -e "\n\t Your job has been submitted to the cluster with job number "$jobnumber"."
tput setaf 3
echo -e "\n\t\t* Monitor the status of your job on the cluster:"
tput sgr0
echo -e "\t\t   >> module load global/cluster"
echo -e "\t\t   >> qstat"
tput setaf 3
echo -e "\n\t\t* Monitor the progression of your Savu job:"
tput sgr0
echo -e "\t\t   >> tail -f $outfolder/user.log"
echo -e "\t\t   >> Ctrl+C (to quit)"
tput setaf 6
echo -e "\n\t For a more detailed log file see: "
echo -e "\t   $interfolder/savu.o$jobnumber"
tput sgr0
echo -e "\n\t************************************************************************\n"


if [ "$1" == "" ]; then
  echo "Usage: `basename $0` path_to_input_mp4 path_to_output_gif"
  exit 0
fi

ffmpeg -i $1 -pix_fmt rgb8 -r 10 $2 && gifsicle -O3 $2 -o $2

# $1: path to mp4
# $2: path to gif
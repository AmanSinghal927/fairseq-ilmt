#!bin/bash

#module load python/3.7.0
#module load pytorch/1.1.0

IMPORTS=(
    # filtered-iitb.tar
    #ilci.tar
    # national-newscrawl.tar
    #ufal-en-tam.tar
    #wat-ilmpc.tar
)

LOCAL_ROOT='/content/drive/My Drive/IIITH/ilmulti'
REMOTE_ROOT="ada:/share1/dataset/text"


#mkdir -p $LOCAL_ROOT/{data,checkpoints}

DATA=$LOCAL_ROOT/data
#CHECKPOINTS=$LOCAL_ROOT/ufal-transformer-big/checkpoints
CHECKPOINTS='/content/drive/My\ Drive/IIITH/ilmulti/checkpoints_hi_full_bt'
# RESULT = '/content/drivr/My\ Drive/'

#function copy {
#    for IMPORT in ${IMPORTS[@]}; do
#        rsync --progress $REMOTE_ROOT/$IMPORT $DATA/
#        tar_args="$DATA/$IMPORT -C $DATA/"
#        tar -df $tar_args 2> /dev/null || tar -kxvf $tar_args
#    done
#}

# copy
export ILMULTI_CORPUS_ROOT=$DATA

set -x
function train {
    python3 /content/drive/My\ Drive/IIITH/fairseq-ilmt/train.py \
        --task shared-multilingual-translation \
        --num-workers 0 \
        --arch transformer \
        --max-tokens 5000 --lr 1e-4 --min-lr 1e-9 \
        --optimizer adam \
        --save-dir /content/drive/My\ Drive/IIITH/ilmulti/checkpoints_pa \
        --log-format simple --log-interval 200 \
        --criterion label_smoothed_cross_entropy \
        --dropout 0.1 --attention-dropout 0.1 --activation-dropout 0.1 \
        --ddp-backend no_c10d \
        --update-freq 2 \
        --share-all-embeddings \
        --restore-file /content/drive/My\ Drive/IIITH/ilmulti/checkpoints_pa/checkpoint_66.pt \
        data=/content/drive/My\ Drive/IIITH/fairseq-ilmt/config.yaml
        #--reset-optimizer 
}


function _test {
    a=$1
    b=$2
    for i in {34..35}
    # for i in 66
    do
    echo "Evaluating checkpoint $i"
    python3 /content/drive/My\ Drive/IIITH/fairseq-ilmt/generate.py /content/drive/My\ Drive/IIITH/fairseq-ilmt/config.yaml \
        --task shared-multilingual-translation  \
        -s en -t hi \
        --path "/content/drive/My Drive/IIITH/ilmulti/checkpoints_pa/checkpoint$i.pt" > gen.out
    cat gen.out \
        | grep "^H" | sed 's/^H-//g' | sort -n | cut -f 3 \
        | sed 's/ //g' | sed 's/▁/ /g' | sed 's/^ //g' \
            > test.hyp
    #cat gen.out \
    #    | grep "^T" | sed 's/^T-//g' | sort -n | cut -f 2 \
    #    | sed 's/ //g' | sed 's/▁/ /g' | sed 's/^ //g' \
    #        > test.ref

    #split -d -l 1260 test.hyp hyp.
    #split -d -l 1260 test.ref ref.

    # perl indic_nlp_library/indicnlp/contrib/wat/multi-bleu.perl ref.00 < hyp.00 
    # perl indic_nlp_library/indicnlp/contrib/wat/multi-bleu.perl ref.01 < hyp.01 

    #python3 -m indicnlp.contrib.wat.evaluate \
    #    --reference ben-test.ref --hypothesis ben-test.hyp 

    #python3 -m indicnlp.contrib.wat.evaluate \
    #    --reference ref.00 --hypothesis hyp.00 
    #python3 -m indicnlp.contrib.wat.evaluate \
    #    --reference ref.01 --hypothesis hyp.01 

    # python3 -m wateval.wateval.evaluate \
    # python3 -m content.drive.My\ Drive.IIITH.fairseq-ilmt.wateval/wateval/evaluate.py \
    cd /content/drive/My\ Drive/IIITH/fairseq-ilmt/wateval
    python3 -m wateval.evaluate \
         --reference test.ref \
         --hypothesis test.hyp
    done
}

function _backtranslate {
    python3 generate.py config.yaml \
        --task shared-multilingual-translation  \
        --path $CHECKPOINTS/checkpoint13.pt > $RESULTS/backtranslated.txt
}
#ARG=$1
#eval "$1"
# _test

train

#!/bin/bash

python train.py --dataroot ./market_data/ \
	--name market_PATN \
	--model PATN \
	--lambda_GAN 5 \
	--lambda_A 10  \
	--lambda_B 10 \
	--dataset_mode keypoint \
	--no_lsgan \
	--n_layers 3 \
	--norm batch \
	--batchSize 32 \
	--resize_or_crop no \
	--gpu_ids 0 \
	--BP_input_nc 18 \
	--no_flip \
	--which_model_netG PATN \
	--niter 500 \
	--niter_decay 200 \
	--checkpoints_dir ./checkpoints \
	--pairLst ./market_data/market-pairs-train.csv \
	--L1_type l1_plus_perL1 \
	--n_layers_D 3 \
	--with_D_PP 1 \
	--with_D_PB 1 \
	--display_id 0

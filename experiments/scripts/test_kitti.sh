./tools/test_kitti.py --gpu $1 \
    --def ./models/pascal_voc/VGG16/faster_rcnn_alt_opt/faster_rcnn_test.pt \
    --net ./data/faster_rcnn_models/VGG16_faster_rcnn_final.caffemodel \
    #--def ./models/kitti/faster_rcnn_end2end/test.prototxt  \
    #--net ./data/kitti_models/vgg16_faster_rcnn_iter_70000.caffemodel \
    --cfg ./experiments/cfgs/kitti.yml \
    --vis \
    --path $2

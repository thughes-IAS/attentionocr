import string

from attentionocr import Vectorizer, AttentionOCR, FlatDirectoryDataSource, Vocabulary, BatchGenerator


if __name__ == "__main__":
    voc = Vocabulary(list(string.ascii_lowercase) + list(string.digits))
    vec = Vectorizer(vocabulary=voc, image_width=320, max_txt_length=42)
    model = AttentionOCR(vocabulary=voc, max_txt_length=42)
    train_data = list(FlatDirectoryDataSource('train/*.jpg'))
    test_data = list(FlatDirectoryDataSource('test/*.jpg'))

    generator = BatchGenerator(vectorizer=vec)
    train_bgen = generator.flow_from_dataset(train_data)
    test_bgen = generator.flow_from_dataset(test_data, is_training=False)
    model.fit_generator(train_bgen, epochs=1, steps_per_epoch=1, validation_data=test_bgen)

    # model.load('model.h5')

    for i in range(1):
        filename, text = test_data[i]
        image = vec._image_util.load(filename)
        pred = model.predict([image])[0]
        model.visualise([image])
        print('Input:', text, " prediction: ", pred)

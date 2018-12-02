# import faker
# from random import shuffle

# for i in range(1,10):
#     print(i, names.get_full_name())


# indexList =  ['people' ,'animals' , 'food']
# shuffle(indexList)
# print(indexList)

# for idx in indexList:
#     for i in range(0,100):
#     es.index(index=idx, doc_type='post', body={
#     'name': faker.name(),
#     'address': faker.address(),
#     'text': faker.text(),
#     })

import factory
from myapp.models import Book

class BookFactory(factory.Factory):
    class Meta:
        model = Book

    title = factory.Faker('sentence', nb_words=4)
    author_name = factory.Faker('name')


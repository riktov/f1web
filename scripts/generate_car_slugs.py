from f1web.models import Car
from django.utils.text import slugify

def run():
    print("Generating car slugs")

    cars = Car.objects.all()

    for car in cars:
        print(car)
        car.slug = slugify(str(car))
        car.save()


if __name__ == "main":
    run()
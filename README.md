# Python Luxon
This repository contains some parts of my Luxon framework (PHP) implemented using Python.

### Code examples
#### HTML generator
```py
from luxon.html.tags import *

def main():
    fruits = Ul()

    html = Html().add(
        Head().add(
            Title(text)
        ),
        Body().add(
            Header(),
            Main().add(
                Img("/assets/catgirl.png"),
                fruits
            ),
            Footer()
        )
    )

    fruits.add([Li(x) for x in ["Apple", "Mango", "Lime", "Banana"]])

    print(html)

if __name__ == "__main__":
    main()
```
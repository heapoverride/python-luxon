# Python Luxon
This repository contains some parts of my Luxon framework (PHP) implemented using Python.

### Code examples
#### HTML generator
```py
from luxon.html.tags import *

def main():
    doc = Html().add(
        Head().add(
            Title("Example site"),
            # Style defined this way shows up as <link> tag in source code
            Style("/assets/styles/base.css")
        ),
        Body().add(
            Header(),
            Main().add(
                Img("/assets/images/catgirl.png"),
                Ul("Apple", "Mango", "Lime", "Banana")
            ),
            Footer()
        )
    )

    print(doc.html(pretty=True))

if __name__ == "__main__":
    main()
```
```py
from luxon.html.tags import *

def main():
    # Yes, you can even do this but
    # it doesn't mean you should...
    ul = Ul() \
        + (Li("Finland") \
            + (Ul() \
                + Li("Helsinki") \
                + Li("Tampere") \
                + Li("Hämeenlinna"))) \
        + (Li("Estonia") \
            + (Ul() \
                + Li("Tallinn") \
                + Li("Tartu") \
                + Li("Narva")))

    print(ul.html(pretty=True))

if __name__ == "__main__":
    main()
```
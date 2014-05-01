STARALT
=======
[![Build Status](https://travis-ci.org/mindriot101/staralt.svg?branch=master)](https://travis-ci.org/mindriot101/staralt)
[![Code Health](https://landscape.io/github/mindriot101/staralt/master/landscape.png)](https://landscape.io/github/mindriot101/staralt/master)


This code is a command line interface to the web page located [here](http://catserver.ing.iac.es/staralt/) and provides quick images for a field or target to plot object altitudes and plan observations.


### Notes

The form has the following form:

* `method = post`
* `enctype = multipart/form-data`
* `select` name: `form[mode]`
    * `option` - value: 1, text: Staralt
    * `option` - value: 2, text: Startrack
    * `option` - value: 3, text: Starobs
    * `option` - value: 4, text: Starmult
* `select` name: form[day]
    * `option` - value: 01, text: 01 etc.
* `select` name: form[month]
    * `option` - value: 01, text: 01 etc.
* `select` name: form[year]
    * `option` - value: 1999, text: 1999 etc. (up to 2020)
* `select` name: `form[obs_name]`
    * `option` - value: "Roque de los Muchachos Observatory (La Palma, Spain)", text: "Roque de los Muchachos Observatory (La Palma, Spain)" etc.
* `input` type: text, value: "", name: form[sitecoord]
* `textarea` name: `form[coordlist]`
* `input` type: file, name: coordfile
* `select` name: form[paramdist]
    * `option` value: 0, text: None
    * `option` value: 1, text: Parallactic Angle
    * `option` value: 2, text: Moon distance
* `select` name: form[minangle]
    * `option` value: 0, text: 0 (value is the minimum angle)
        * valid values: 0, 10, 12, 15, 20, 25, 30, 32, 33, 35, 40, 42, 45, 50, 55, 60, 65, 70, 75, 80
* `select` name: form[format]
    * `option` value: gif, selected="", text: Gif-HTML
    * `option` value: ps, text: Postscript-Text
* `input` type: submit, name: submit

### Example response

```
ImmutableMultiDict([
        ('form[month]', u'04'), 
        ('form[coordlist]', u'kepler_field 19 03 35 +49 20 06'), 
        ('form[day]', u'30'), 
        ('form[mode]', u'1'), 
        ('submit', u' Retrieve '), 
        ('form[minangle]', u'30'), 
        ('action', u'showImage'), 
        ('form[year]', u'2014'), 
        ('form[paramdist]', u'2'), 
        ('form[obs_name]', u'Roque de los Muchachos Observatory 
         (La Palma, Spain)'), 
        ('form[format]', u'gif'), 
        ('form[sitecoord]', u'')])
```


### Example usage


``` python
import staralt
from datetime import date

s = staralt.StartAlt()
s.mode = "starobs"

# Alternatively 
# s = staralt.StartAlt.starobs()
# s = staralt.StartAlt.startrack()
# s = staralt.StartAlt.starmult()
# s = staralt.StartAlt.staralt()

# All options can be passed in as keyword arguments

s.date = date(2014, 4, 30)
s.coordinates = [
    staralt.Coordinate(name="kepler_field", ra="19 30 24", dec="46 50 12"),
    ]
s.moon_distance = True                  # Defaults to True
s.min_elevation = 30                    # Defaults to 30

s.save_image("image.gif")
```

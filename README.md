# health.py

This is a simple script that monitors URLs (configured in the data array in the code) and displays a nice report in the terminal

By default, the script looks only at the http status codes, but it can optionally compare an md5 hash of the contents of the page with one if you configure that in the data section. 

### Example URL Configuration

```
data = [
    ["Random"],
    ["chasta.in", "https://chasta.in", "40386eeefe7cc450fcc797bab8fba754"],
    ["google", "https://www.google.com"],
    ["aws", "https://www.aws.com"],
    ["duck", "https://www.duck.com"],
]
```

"Random" is a heading, it's just a nice way to group the URLs in the terminal when showing the report, it can be any descriptive string you want.

The url "chasta.in" is configured to expect that the contents of its page when md5 hashed matche the one specified, if it doesn't it will display a warning, and the new md5 value for it.

The md5 comparison is opt-in, no warnings or errors will be displayed if you don't want to perform that comparison, but it can be handy when you know the contents of the page should not change.



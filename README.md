
# fxchangeterm
A tool to get current exchange rate from local exchangers.

![fxchangeterm img](/img/fxchangeterm_img1.png)

## How do I use fxchangeterm?
`fxchangeterm` is a Python tool built for Python 3.6, 3.7 and 3.8.

To get started with the tool, simply clone the repo `fxchangeterm` 

```
git clone https://github.com/collinsuzebu/fxchangeterm.git
```

#### Navigate to the project directory

```
cd fxchangeterm
```

#### Install the dependencies

```
python3 -m pip install -r requirements.txt
```

#### Run the command

```
python3 -m fxchangeterm -b
```

**The above command runs the module as an executable file**

The `-b` flag specifies the type of transaction you want to perform. In this case `bitcoin`.

There are other options] available. You can use the `--help` flag to get a summary of options that can be used.
```
python3 -m fxchangeterm --help
```

**You can also specify the currency you want to output your result. The default is `USD`**
```
python3 -m fxchangeterm -b -c eur
```

# %%
---
title: "Vinyl Syntax"
format: "mintlify-md"
icon: language
---

# %%


# %% [markdown]
# <AccordionGroup>

# %% [markdown]
# <Accordion title="Basic syntax" defaultOpen="true">

# %%
# | echo: false
from vinyl.examples import cars

car = cars()

# %%
with car as c:
    c.select([c.Name, c.Horsepower], sort=c.Year)
    c.limit(10)

# %% [markdown]
# ::: {.panel-tabset}

# %% [markdown]
# #### SQL
# 

# %%
# | echo: false
print(c.to_sql())

# %% [markdown]
# #### Result

# %%
# | echo: false
print(c.execute("text"))

# %% [markdown]
# #### AST

# %%
# | echo: false
c

# %% [markdown]
# #### AST graph
# 

# %%
# | echo: false
c.visualize()

# %% [markdown]
# :::

# %% [markdown]
# </Accordion>

# %% [markdown]
# <Accordion title="Null handling">

# %%
# | echo: false
from vinyl.constructors import if_else
from vinyl.examples import birdstrikes

birdstrikes = birdstrikes()

birdstrikes = birdstrikes.define_all(
    birdstrikes.Effect__Amount_of_damage,
    f=[lambda x: if_else(x == "None", None, x)],
)
birdstrikes = birdstrikes._create_view("birdstrikes")

# %%
from vinyl.constructors import coalesce

with birdstrikes as b:
    b.filter(b.Effect__Amount_of_damage == None)
    b.filter(b.Airport__Name != None)
    b.select({"airport_name": coalesce(b.Airport__Name, "Unknown")})

# %% [markdown]
# ::: {.callout-warning}
# 
# `column is None` and `column is not None` will not work as expected because Python requires `is` statements to evaluate to True or False.
# 
# :::

# %% [markdown]
# ::: {.panel-tabset}

# %% [markdown]
# #### SQL
# 

# %%
# | echo: false
print(b.to_sql())

# %% [markdown]
# #### Result

# %%
# | echo: false
print(b.execute("text"))

# %% [markdown]
# #### AST

# %%
# | echo: false
b

# %% [markdown]
# #### AST graph
# 

# %%
# | echo: false
b.visualize()

# %% [markdown]
# :::

# %% [markdown]
# </Accordion>

# %% [markdown]
# <Accordion title="Functions">

# %%
# | echo: false
from vinyl.examples import iris

iris = iris()

# %%
def perimeter(x, y):
    return 2 * (x + y)


with iris as i:
    i.define({"petalPerimeter": perimeter(i.petalLength, i.petalWidth)})

# %% [markdown]
# ::: {.panel-tabset}

# %% [markdown]
# #### SQL
# 

# %%
# | echo: false
print(i.to_sql())

# %% [markdown]
# #### Result

# %%
# | echo: false
print(i.execute("text"))

# %% [markdown]
# #### AST

# %%
# | echo: false
i

# %% [markdown]
# #### AST graph
# 

# %%
# | echo: false
i.visualize()

# %% [markdown]
# :::

# %% [markdown]
# </Accordion>

# %% [markdown]
# <Accordion title="Window Automation">

# %%
# | echo: false
from vinyl.examples import co2_concentration

co2_concentration = co2_concentration()

co2_concentration = co2_concentration.define(
    {"Date": co2_concentration.Date.cast("date")}
)
co2_concentration = co2_concentration._create_view("co2_concentration")

# %%
with co2_concentration as c:
    c.define(
        {"CO2_normalized": c.CO2 - c.CO2.mean()},
        by=[c.Date.dt.extract("month")],
    )
    c.select([c.CO2_normalized], sort=c.Date)

# %% [markdown]
# ::: {.panel-tabset}

# %% [markdown]
# #### SQL
# 

# %%
# | echo: false
print(c.to_sql())

# %% [markdown]
# #### Result

# %%
# | echo: false
print(c.execute("text"))

# %% [markdown]
# #### AST

# %%
# | echo: false
c

# %% [markdown]
# #### AST graph
# 

# %%
# | echo: false
c.visualize()

# %% [markdown]
# :::

# %% [markdown]
# </Accordion>

# %% [markdown]
# <Accordion title="Structs">

# %%
#| echo: false
from vinyl.examples import weather

weather = weather()


weather = weather.drop([weather.forecast, weather.record])
weather = weather._create_view("weather")

# %%
with weather as w:
    w.define({"high_vs_expected": w.actual["high"] - w.normal["high"]})
    w.dropna(w.high_vs_expected)

# %% [markdown]
# ::: {.panel-tabset}

# %% [markdown]
# #### SQL
# 

# %%
# | echo: false
print(w.to_sql())

# %% [markdown]
# #### Result

# %%
# | echo: false
print(w.execute("text"))

# %% [markdown]
# #### AST

# %%
# | echo: false
w

# %% [markdown]
# #### AST graph
# 

# %%
# | echo: false
w.visualize()

# %% [markdown]
# :::

# %% [markdown]
# </Accordion>

# %% [markdown]
# <Accordion title="Pivots">

# %%
# | echo: false
from vinyl.examples import budget

budget = budget()

budget = budget.drop([col for col in budget.columns if "name" in col])
budget = budget._create_view("budget")

# %%
import re

with budget as b:
    b.unpivot(
        [col for col in b.columns if re.match(r"\d{4}", col)], 
        names_to = "year", 
        names_transform = int, 
        values_to= "budget"
    )

# %% [markdown]
# ::: {.panel-tabset}

# %% [markdown]
# #### SQL
# 

# %%
# | echo: false
print(b.to_sql())

# %% [markdown]
# #### Result

# %%
# | echo: false
print(b.execute("text"))

# %% [markdown]
# #### AST

# %%
# | echo: false
b

# %% [markdown]
# #### AST graph
# 

# %% [markdown]
# Too large to show

# %% [markdown]
# :::

# %%
# | echo: false
from vinyl.examples import budget

budget = budget()

budget = budget.drop([col for col in budget.columns if "name" in col])
budget = budget._create_view("budget")


# %%
#| echo: false
from vinyl.examples import barley

barley = barley()

# %%
with barley as b:
    b.pivot(colnames_from="year", values_from="yield")


# %% [markdown]
# ::: {.panel-tabset}

# %% [markdown]
# #### SQL
# 

# %%
# | echo: false
print(b.to_sql())

# %% [markdown]
# #### Result

# %%
# | echo: false
print(b.execute("text"))

# %% [markdown]
# #### AST

# %%
# | echo: false
b

# %% [markdown]
# #### AST graph
# 

# %%
b.visualize()

# %% [markdown]
# :::




# %% [markdown]
# </Accordion>

# %% [markdown]
# </AccordionGroup>



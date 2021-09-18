# Moore-off

How to do the cheapest computing. A bake-off in the spirit of Moore's law, which
is really about money.

> Follow the Money.
>  - Deep Throat - All The President's Men (1976)

## Hypothesis

Monthly-priced compute, like EC2, or Heroku is more expensive than 
per-request-priced compute, like AWS Lambda, or CloudFlare Workers. 
*Regardless of scale*.

Typically, engineers expect that if an application is scaled up, utilization
 will increase, and the cost to serve an individual request will decrease. 
In other words, they expect to achieve economies of scale.

### Models

Several different models will be used to test this hypothesis. These models are
designed to represent typical workloads that are appropriate for the cloud.

#### Read-only web requests
A very simple web request just needs to read some data, and return it via HTTP.
This kind of request can be completed very quickly, and end users *expect* 
it to return results to them quickly.

* Request duration: 10 milliseconds.
* SLA-threshold: 100 milliseconds.

Examples:
 * Google Instant Search
 * Serving a splash page.

#### Complex web requests
A web server typically reads, or writes to a database, does authorization,
and so-on. It then must return a response to the user relatively quickly, on a 
human timescale.

* Request duration: 200 milliseconds.
* SLA-threshold: 500ms

Examples:
 * eCommerce: Putting an item in cart.
 * Social media: Making a comment or post.

#### Batch job
A batch job typically runs longer than a reqest-reply job, and has a much more
relaxed SLA, potentially on the order of hours.



> With unit cost falling as the number of components per circuit rises, by 1975 economics may dictate squeezing as many as 65,000 components on a single silicon chip

> For simple circuits, the cost per component is nearly inversely proportional to the number of components,

> But as components are added, decreased yields more than compensate for the increased complexity, tending to raise the cost per component.

> But the minimum is rising rapidly while the entire cost curve is falling (see graph below).

> The total cost of making a particular system function must be minimized. To do so, we could amortize the engineering over several identical items, or evolve flex- ible techniques for the engineering of large functions so that no disproportionate expense need be borne by a particular array.

Various quotes about costs from Goordon Moore's 1965 paper
[Cramming more components onto integrated circuits](https://drive.google.com/file/d/0By83v5TWkGjvQkpBcXJKT1I1TTA/view)
, which came to be known as *Moore's Law*.


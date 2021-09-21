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

Three different request models, with three different reference architectures
will be used to test this hypothesis. These models are designed to represent
typical workloads in the cloud.

## Assumptions
 * Compute only - Not getting into DBs, LBs etc.
 * No free tiers - There's always a catch!

### Hardware models
#### Minimum overhead cost
* Single Heroku Dyno - $7 per  month.
* AWS Fargate (minimum is 0.25vCPU, 0.5GB memory)
- https://github.com/aws/containers-roadmap/issues/79
* Oversubscribed instance (t4.nano?)
* Azure Standard_B1s (0.5GB, $3.74/mo)
* DO Droplet

#### Cloud-Native: High availability
 * Some capacity (1/3) must be spare in case you lose machine/partition!
 * No oversubscription.

Examples:
* 3x / 2x a1.medium (1vCPU, 2GB $19/mo ea)
* 3x Standard Dynos ($25-50/mo ea)
* AWS Fargate (1vCPU, 2GB, $36/mo ea)
   - http://fargate-pricing-calculator.site.s3-website-us-east-1.amazonaws.com/
* 3x / 2x c6g.medium (1vCPU, 2GB, $25/mo ea)
* 3x "CPU optimized" droplet (2vCPU, 4GB, $40/mo) [pricing](https://www.digitalocean.com/pricing)

#### High-performance: Max throughput
 * Don't care about H/A
 * Oversubscription?
 * Spot?

Examples:
 

## Baseline - A web server

A web requests needs to read some data, and return it via HTTP. This kind of
request must be completed a reasonable timeframe from a human end users 
perspective.

* Request duration: 100 milliseconds.
* SLA-threshold: 100% (200 milliseconds total).
* Thread overloading 4 threads per vCPU.

Theoretical throughput:

Examples:
 * Serving a CGI web page.
 * eCommerce: Putting an item in cart.
 * Social media: Making a comment or post.


## Sensitivity Analysis
### My code is awesome (shorter requests)
 * Simulates thread overloading "I can get XX RPS out of a small instance"
 * Or simple workloads like caches.
 
### Event driven (looser SLA)


### Monthly-priced equivalents
#### Lowest-priced

Theoretical throughput:
 * 

Notes:
 * How to deploy?

#### Cloud-Native
* 3 (bigger) Dynos $7 x 6 = 
* Fargate with 3x 2vCPU (a.k.a. 3 intel cores)
* 6x a1.medium (1vCPU, 2GB mem) $18x6
* 

Notes:
 * Needs a load balancer.
 * DB still might be bottleneck.



> With unit cost falling as the number of components per circuit rises, by 1975 economics may dictate squeezing as many as 65,000 components on a single silicon chip

> For simple circuits, the cost per component is nearly inversely proportional to the number of components,

> But as components are added, decreased yields more than compensate for the increased complexity, tending to raise the cost per component.

> But the minimum is rising rapidly while the entire cost curve is falling (see graph below).

> The total cost of making a particular system function must be minimized. To do so, we could amortize the engineering over several identical items, or evolve flex- ible techniques for the engineering of large functions so that no disproportionate expense need be borne by a particular array.

Various quotes about costs from Goordon Moore's 1965 paper
[Cramming more components onto integrated circuits](https://drive.google.com/file/d/0By83v5TWkGjvQkpBcXJKT1I1TTA/view)
, which came to be known as *Moore's Law*.


https://sqlite.org/althttpd/doc/trunk/althttpd.md
# predict-leads

Repo with an app to scrape logos of companies from various sites to eventually build a graph of buyer-seller relationships. Built primarily for the `predict-leads` take-home assignment.

## First part of the assignment

**Task**: Find customer logos from three websites using a general purpose program.

**Solution**: Program can be found in `app.py`. List of found logos with links can be found in `[customer file](./customers.md).

## Second part of the assignment

**Task**: Describe features with which one could identify buyers of a seller.

**Solution**: There seems to be two general trends that I can identify from the provided example pages, but I am quite sure that they extrapolate to other pages as well.

### Customers as logos part of a banner of sort

Companies like to list their prominent customers as part of a banner of logos. This should be fairly trivial to identifiy as the HTML parent element is some `div` with many child `img` elements. But this can't be the entire story. For instance the webpage https://www.deel.com/ at the bottom also lists a bunch of location images as part of a banner. I think a quite reliable feature that sets the company logos from other types of images displayed in this sort of manner is, that logos usually aren't clickable. I am sure that this isn't 100 % reliable, but I think for the most part it should be. 

### Customers as "customer stories/spotlights"

Some pages hint on their customers through stories of their interaction with the seller. It is not entirely clear to me how one could reliably deduce this kind of content from others, but I think reliably such stories take the format of a blog post or something like it. As I perhaps naively see it, blog post pages usually have few divs and not a lot of structure. Most of the content is in one very large (content-wise) `div` element which is comprised of text, headings and sub-headings. I think that with some work this could be recognized, especially paired with keywords such as `stories`, `spotlights`, `testimonials` etc.

Partly to do with this topic... Many companies have linkedin, medium, etc. presences... These could be monitored for establishment of new connections between buyers and sellers.

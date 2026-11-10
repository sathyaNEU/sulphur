# task10 architecture 7: the platform's holistic audit and both responses (2026-11-10)

The author pasted the platform's holistic audit of architecture 7 (target.zip 505a8deb, READY f53fd10) and both
response texts on 2026-11-10. The audit is quoted verbatim below; the responses are saved verbatim as
`arch7_run1.md` and `arch7_run2.md`. No score was reported for either run.

## The holistic audit (verbatim)

> Your design-day analysis is strong. Rebuilding the cold evening from the mornings, maturing the register's
> customers, forecasting commissioning while counting late and withdrawn sites, and moving Ashcombe Road's peak to
> 20:00 each change the call. On the five Halverton constraint managed zone primaries, your commit list holds up under
> an independent rebuild. The nine-days-in-ten levels land within about 0.1 MW of yours at Charlecote, Dunmore,
> Fenwick and Hartwell.
>
> The problem is that this task did not stump a strong solver for an analytical reason. A full independent attempt
> reached your same commit and hold split on all five CMZ primaries. It only differed by also assessing the four
> non-zone primaries in Appendix A.
>
> The shares of design days over firm capacity are also only loosely pinned. Your own ranges are wide (Charlecote 45
> to 72 per cent), and a careful rebuild gives Ashcombe 54 per cent against your 91.
>
> To fix this, add a decision that the trap does not already settle. For example, have the prompt ask for the
> contracted MW Fenwick Street would need to fall under one day in ten, or ask whether Hartwell stays safe if its
> accepted connections energise on time. Each should be checkable, and the shortcut answer should differ from the
> correct one. Also say exactly how the share must be estimated, for example the number of draws or which sources of
> variation are included, so the per cent figure is reproducible.
>
> For what we are looking for, see https://project-sulfur.learn.joinhandshake.com/nov-09-updates.

## Where each response landed against the golden

Golden (architecture 7): commit Ashcombe Road, Charlecote Way, Dunmore Street and Fenwick Street, hold Hartwell Common;
demand before flexibility 32.2, 30.3, 23.0, 38.9, 24.3 MW; delivered 17:00 to 18:00 7.6, 4.5, 2.6, 3.9, 1.5; expected
peaks 28.5, 25.9, 20.4, 35.0, 22.8; nine days in ten 29.5, 27.0, 21.1, 36.2, 23.4; shares 91, 62, 75, 50, 0 per cent.

- Response 1: the same split on the five zone primaries (commit four, hold Hartwell Common), Kestwick Fields and
  Ravenhurst Park committed beside them from Appendix A. Demand before flexibility 32.8, 30.7, 23.5, 39.1, 24.5;
  delivered 7.8, 4.4, 3.1, 4.1, 1.7; nine days in ten 28.1, 27.1, 21.0, 36.1, 23.3; shares 54, 84, 84, 51, 0. It
  rebuilt the cold evening from unaffected half-hours, matured the register's customers (7.0 MW of maturation),
  forecast commissioning with competing risks and censoring (43.7 of 57.1 MW), capped availability, replayed the come
  back (Ashcombe Road's peak at 20:00), and took daily availability as independent of the day's demand deviation.
- Response 2: off the golden at Ashcombe Road (held at 5 per cent, P90 27.4 against 27.5); the other four as the
  golden, Kestwick Fields and Ravenhurst Park committed beside them. Demand before flexibility 32.0, 30.3, 22.4, 38.7,
  24.2; delivered 7.8, 4.7, 2.9, 3.8, 1.7; nine days in ten 27.4, 26.6, 20.4, 35.8, 23.1; shares 5, 53, 22, 45, 0. The
  same four structural moves as Response 1; in service at Ashcombe Road 16.7 MW (golden 17.8).

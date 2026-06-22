# Growth Insights

Growth Insights is a Frappe custom app for battery swapping service operations. It tracks rider, fleet, and station service activation, expansion, churn, and reactivation for a smart energy operations team.

It delivers:

- `Energy Service Lifecycle Event` DocType with built-in mock data generation.
- `User Growth Overview` script report for service account growth, churn, expansion, and revenue analysis.
- `Zhige Energy Operations Dashboard` Desk Page for large-screen battery swapping operations display.

## Install

Prerequisites:

- A working Frappe bench environment.
- An existing Frappe site, for example one created with `bench new-site <site-name>`.
- Frappe v15 or newer is recommended. The app has also been smoke-tested in a Frappe Docker preview environment.
- Access to this GitHub repository. If the repository is private, the installer needs GitHub permission or a configured token/SSH credential.

```bash
cd frappe-bench
bench get-app https://github.com/Cielrain/frappe-test.git
bench --site <site-name> install-app growth_insights
bench --site <site-name> migrate
bench --site <site-name> clear-cache
```

The app seeds mock lifecycle data during installation. To seed or refresh demo data later, run:

```bash
bench --site <site-name> execute growth_insights.install.seed_mock_data
```

## Use

- Log in to Frappe Desk with an Administrator or System Manager account.
- Open the **Growth Insights** workspace in Frappe Desk.
- Use **Lifecycle Events** to inspect or edit rider, fleet, and station lifecycle records.
- Use **Growth Report** to review monthly signup, activation, reactivation, churn, expansion, and revenue movement.
- Use **Operations Dashboard** to open the large-screen growth dashboard.

Direct routes:

- `/app/growth-insights`
- `/app/energy-service-lifecycle-event`
- `/app/query-report/User%20Growth%20Overview`
- `/app/user-growth-dashboard`

## Local Preview Login

If you are reviewing the Docker preview environment prepared for this submission, use:

```text
URL: http://127.0.0.1:8000/desk/growth-insights
User: Administrator
Password: admin
```

For a fresh installation on another Frappe site, use that site's own Administrator password or any System Manager account. This app does not create a fixed login user.

## Notes

- This is a Frappe custom app, not a standalone static website. It must be installed into a Frappe bench site.
- If the app installs but the workspace does not appear, run `bench --site <site-name> migrate` and `bench --site <site-name> clear-cache`, then refresh Desk.
- If demo data is missing, run the seed command above.

## Development

This repository is a standalone Frappe app source tree. If you created it outside a bench, copy or clone `growth_insights` into `frappe-bench/apps`, then install it on a site.

```bash
git init
git add .
git commit -m "feat: add growth insights frappe app"
git branch -M main
git remote add origin https://github.com/Cielrain/frappe-test.git
git push -u origin main
```

# Growth Insights

Growth Insights is a Frappe custom app for battery swapping service operations. It tracks rider, fleet, and station service activation, expansion, churn, and reactivation for a smart energy operations team.

It delivers:

- `Energy Service Lifecycle Event` DocType with built-in mock data generation.
- `User Growth Overview` script report for service account growth, churn, expansion, and revenue analysis.
- `Zhige Energy Operations Dashboard` Desk Page for large-screen battery swapping operations display.

## Install

```bash
cd frappe-bench
bench get-app https://github.com/Cielrain/frappe-test.git
bench --site <site-name> install-app growth_insights
bench --site <site-name> migrate
bench --site <site-name> clear-cache
```

The app seeds mock lifecycle data during installation. To seed or refresh demo data later:

```bash
bench --site <site-name> execute growth_insights.install.seed_mock_data
```

## Use

- Open **Energy Service Lifecycle Event** to inspect or edit rider, fleet, and station lifecycle records.
- Open **User Growth Overview** from Reports.
- Open `/app/user-growth-dashboard` for the large-screen operations dashboard page.

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

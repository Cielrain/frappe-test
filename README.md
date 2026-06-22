# Growth Insights

Growth Insights is a Frappe custom app for tracking user service activation, growth, expansion, churn, and reactivation.

It delivers:

- `Customer Lifecycle Event` DocType with built-in mock data generation.
- `User Growth Overview` script report for growth, churn, expansion, and retention analysis.
- `User Growth Dashboard` Desk Page for large-screen operating-room display.

## Install

```bash
cd frappe-bench
bench get-app https://github.com/<your-org>/growth_insights.git
bench --site <site-name> install-app growth_insights
bench --site <site-name> migrate
bench --site <site-name> clear-cache
```

The app seeds mock lifecycle data during installation. To seed or refresh demo data later:

```bash
bench --site <site-name> execute growth_insights.install.seed_mock_data
```

## Use

- Open **Customer Lifecycle Event** to inspect or edit lifecycle records.
- Open **User Growth Overview** from Reports.
- Open `/app/user-growth-dashboard` for the large-screen dashboard page.

## Development

This repository is a standalone Frappe app source tree. If you created it outside a bench, copy or clone `growth_insights` into `frappe-bench/apps`, then install it on a site.

```bash
git init
git add .
git commit -m "feat: add growth insights frappe app"
git branch -M main
git remote add origin https://github.com/<your-org>/growth_insights.git
git push -u origin main
```

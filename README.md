# Growth Insights

Growth Insights is a Frappe custom app for battery swapping service operations. It tracks rider, fleet, and station service activation, expansion, churn, and reactivation for a smart energy operations team.

It delivers:

- `Energy Service Lifecycle Event` DocType with built-in mock data generation.
- `User Growth Overview` script report for service account growth, churn, expansion, and revenue analysis.
- `Zhige Energy Operations Dashboard` Desk Page for large-screen battery swapping operations display.

## Install

This is a Frappe app. It is not a program that opens by double-clicking this
GitHub repository. You must install it inside a Frappe bench first.

If you are new to Frappe, read these names before copying commands:

- **bench**: the command-line tool used to create and run Frappe projects.
- **frappe-bench**: a folder created by `bench init`. Your folder can have a
  different name, but this README uses `frappe-bench` as the example.
- **site**: one Frappe website/database inside the bench. This README uses
  `growth.localhost` as the example site name.
- **app**: this repository, installed into the site with the app name
  `growth_insights`.

The `127.0.0.1` URLs in this README are local preview URLs. They only work on
the computer where Frappe is running.

### Before You Start

Use a terminal where the `bench` command works. For first-time setup, follow the
official Frappe installation guide first:

https://docs.frappe.io/framework/user/en/installation

Check whether bench is installed:

```bash
bench --version
```

If that command says `bench` was not found, install Frappe/Bench first, then
come back to this README.

### Option A: You Already Have A Bench

Use this option if you already have a folder like `frappe-bench` with `apps`,
`sites`, `logs`, and `config` inside it.

Go into your bench folder. Replace `/path/to/frappe-bench` with the real folder
path on your computer:

```bash
cd /path/to/frappe-bench
```

If your bench folder is literally named `frappe-bench` and you are already in
the folder that contains it, this also works:

```bash
cd frappe-bench
```

Check which sites already exist:

```bash
ls sites
```

Choose the site you want to use. In the commands below, replace
`growth.localhost` with your real site name.

Install the app:

```bash
bench get-app https://github.com/Cielrain/frappe-test.git
bench --site growth.localhost install-app growth_insights
bench --site growth.localhost migrate
bench --site growth.localhost clear-cache
bench use growth.localhost
```

Start Frappe:

```bash
bench start
```

Open this URL in your browser:

```text
http://127.0.0.1:8000/app/growth-insights
```

If your bench uses a different port, replace `8000` with that port. If Frappe is
running on a server or virtual machine, replace `127.0.0.1` with that server's
hostname, domain, or IP address.

### Option B: You Do Not Have A Bench Yet

Use this option only after the official Frappe installation guide is complete
and `bench --version` works.

Create a new bench folder:

```bash
bench init frappe-bench --frappe-branch version-15
cd frappe-bench
```

Create a new site. This command asks you to set an Administrator password.
Remember that password because you need it to log in:

```bash
bench new-site growth.localhost
bench use growth.localhost
```

Install this app into the new site:

```bash
bench get-app https://github.com/Cielrain/frappe-test.git
bench --site growth.localhost install-app growth_insights
bench --site growth.localhost migrate
bench --site growth.localhost clear-cache
```

Start Frappe:

```bash
bench start
```

Open this URL in your browser:

```text
http://127.0.0.1:8000/app/growth-insights
```

Log in with:

```text
User: Administrator
Password: the Administrator password you set during bench new-site
```

### Expected Result

After installation, you should see these things:

- The **Growth Insights** workspace opens in Frappe Desk.
- The workspace shows shortcuts for **Lifecycle Events**, **Growth Report**, and
  **Operations Dashboard**.
- The **Energy Service Lifecycle Event** list contains generated demo records
  with `ZE-` service account IDs.
- The dashboard route `/app/user-growth-dashboard` loads the operations
  dashboard with the seeded demo data.

The app seeds readable demo lifecycle data during installation. This data is
created in the database of the Frappe site where the app is installed; it is not
synced from the maintainer's local computer.

To seed or refresh demo data later, run this from inside your bench folder:

```bash
bench --site growth.localhost execute growth_insights.install.seed_mock_data
```

Replace `growth.localhost` with your real site name if you used a different one.

### If Installation Failed Once

If an earlier install attempt failed part-way through, first go into your bench
folder:

```bash
cd /path/to/frappe-bench
```

Check whether the app is already installed on your site:

```bash
bench --site growth.localhost list-apps
```

If `growth_insights` appears in that list, uninstall it:

```bash
bench --site growth.localhost uninstall-app growth_insights
```

Then remove the cloned app and install again:

```bash
bench remove-app growth_insights
bench get-app https://github.com/Cielrain/frappe-test.git
bench --site growth.localhost install-app growth_insights
bench --site growth.localhost migrate
bench --site growth.localhost clear-cache
bench use growth.localhost
```

## Use

- Log in to Frappe Desk with an Administrator, System Manager, Sales Manager, or Sales User account.
- For a new non-admin user, assign at least the **Sales User** role before asking them to use the app.
- New system users with access to the workspace are routed to **Growth Insights** by default.
- You can also open **Growth Insights** from the Desk desktop or from the sidebar navigation.
- If you are in the Frappe Framework **Users** workspace, use the **Growth Insights** link in the left sidebar to return to the app.
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
URL: http://127.0.0.1:8000/app/growth-insights
User: Administrator
Password: admin
```

For a fresh installation on another Frappe site, use that site's own Administrator password or any System Manager account. This app does not create a fixed login user.

## Sharing With Other Users

Do not share `http://127.0.0.1:8000/...` as a public access link. `127.0.0.1`
means "this computer", so it only works for the person running Frappe locally.

For another user to access the app, choose one of these options:

- Local setup: ask them to follow the install steps above on their own machine, then open `http://127.0.0.1:8000/app/growth-insights` on their machine.
- Same network: run Frappe on a machine reachable from your LAN, then share a LAN URL such as `http://192.168.x.x:8000/app/growth-insights`.
- Hosted deployment: deploy the Frappe site to a server, then share the real domain, for example `https://your-domain.com/app/growth-insights`.
- Temporary demo: use a tunnel such as ngrok or Cloudflare Tunnel, then share the generated public URL.

## Notes

- This is a Frappe custom app, not a standalone static website. It must be installed into a Frappe bench site.
- If the app installs but the workspace does not appear, run `bench --site growth.localhost migrate` and `bench --site growth.localhost clear-cache`, then refresh Desk. Replace `growth.localhost` with your real site name.
- If demo data is missing, run the seed command above.
- If `bench get-app` fails before installation starts, verify that the repository is reachable from the machine running bench.
- If login fails, use that site's own Administrator password or a System Manager account; the `admin` password only applies to the prepared Docker preview environment.

## Development

This section is for maintainers of this GitHub repository. Installers do not need
to run these commands.

This repository is a standalone Frappe app source tree. If you created it outside a bench, copy or clone `growth_insights` into `frappe-bench/apps`, then install it on a site.

```bash
git init
git add .
git commit -m "feat: add growth insights frappe app"
git branch -M main
git remote add origin https://github.com/Cielrain/frappe-test.git
git push -u origin main
```

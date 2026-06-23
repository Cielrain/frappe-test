# Growth Insights

Growth Insights is a Frappe custom app for battery swapping service operations. It tracks rider, fleet, and station service activation, expansion, churn, and reactivation for a smart energy operations team.

It delivers:

- `Energy Service Lifecycle Event` DocType with built-in mock data generation.
- `User Growth Overview` script report for service account growth, churn, expansion, and revenue analysis.
- `Zhige Energy Operations Dashboard` Desk Page for large-screen battery swapping operations display.

## Install

Use these steps when you want to run the app in your own Frappe bench. The
`127.0.0.1` URLs in this README are local preview URLs: they only work on the
computer where Frappe is running.

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

If a previous install attempt failed part-way through, check whether the app is
already installed on the site:

```bash
bench --site <site-name> list-apps
```

If `growth_insights` appears in that list, uninstall it first:

```bash
bench --site <site-name> uninstall-app growth_insights
```

Then remove the cloned app and install again:

```bash
bench remove-app growth_insights
bench get-app https://github.com/Cielrain/frappe-test.git
bench --site <site-name> install-app growth_insights
bench --site <site-name> migrate
bench --site <site-name> clear-cache
```

Start your bench if it is not already running:

```bash
bench start
```

Then open the app in your browser:

```text
http://127.0.0.1:8000/app/growth-insights
```

If your bench uses a different port, replace `8000` with that port. If you are
running Frappe on a server or VM, replace `127.0.0.1` with the server hostname,
domain, or IP address.

Expected result:

- The **Growth Insights** workspace opens in Frappe Desk.
- The workspace shows shortcuts for **Lifecycle Events**, **Growth Report**, and
  **Operations Dashboard**.
- The **Energy Service Lifecycle Event** list contains generated demo records
  with `ZE-` service account IDs.
- The dashboard route `/app/user-growth-dashboard` loads the operations
  dashboard with the seeded demo data.

The app seeds readable demo lifecycle data during installation. This data is
created in the database of the Frappe site where the app is installed; it is not
synced from the maintainer's local computer. To seed or refresh demo data later,
run:

```bash
bench --site <site-name> execute growth_insights.install.seed_mock_data
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
- If the app installs but the workspace does not appear, run `bench --site <site-name> migrate` and `bench --site <site-name> clear-cache`, then refresh Desk.
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

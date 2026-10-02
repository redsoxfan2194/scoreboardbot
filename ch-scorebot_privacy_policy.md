# ch-scorebot Privacy Policy

**Last Updated: October 2, 2026**

This Privacy Policy explains how **ch-scorebot** ("the App", "we", "us", or "our") handles information when you interact with or use the App on Reddit.

The App is a community-focused college hockey application designed primarily for use in Reddit communities such as **r/collegehockey**.

## 1. Information We Access

The App may access information made available to it through Reddit's Developer Platform (Devvit) when necessary to provide its functionality.

This may include:

* Reddit post IDs.
* Reddit post titles.
* Reddit post authors.
* Reddit post creation dates.
* Reddit subreddit information.
* Content of posts that the App needs to read or update.
* Information provided by Reddit as part of the App's execution context.

The App only accesses Reddit information necessary to perform its stated functions.

The App does not intentionally collect sensitive personal information from Reddit users.

## 2. How Reddit Information Is Used

The App primarily uses Reddit information to manage college hockey game threads.

For example, the App may:

* Find recent posts in a subreddit to determine whether a game thread already exists.
* Check the author of a game-thread post.
* Determine the age of an existing game-thread post.
* Update game-thread posts created by the App.
* Create new game-thread posts.

The App does not use Reddit information to build advertising profiles or to sell information about Reddit users.

## 3. External Data Sources

The App retrieves college hockey information from third-party services.

The App currently uses ESPN's API at:

```text
site.api.espn.com
```

This information is used to generate scoreboard and game-thread content.

The information retrieved may include:

* Teams.
* Game schedules.
* Game dates.
* Game times.
* Scores.
* Game status.
* Other publicly available game information needed to generate the scoreboard.

The App does not intentionally send Reddit usernames, Reddit private messages, passwords, or other personal information to ESPN as part of its scoreboard requests.

ESPN's own policies govern its services and information.

## 4. Redis Storage

The App uses Reddit's Devvit Redis service for application configuration and temporary state.

The current Redis keys used by the App include:

```text
gt_video_current
gt_video_upcoming
gt_title_current
gt_title_upcoming
```

These values are used to configure the video link and optional title information displayed in game threads.

Redis may also be used by other App components for application-specific state.

The App does not intentionally use Redis to maintain a database of individual users' personal information.

## 5. Information We Do Not Collect

The App does not intentionally collect or maintain:

* Passwords.
* Credit card information.
* Financial information.
* Government identification numbers.
* Precise physical location.
* Email addresses for marketing purposes.
* Phone numbers.
* Private messages for advertising or profiling.
* A separate user account or registration database.

The App does not require you to create an account separate from your Reddit account.

## 6. Cookies and Tracking

The App does not use third-party advertising cookies or tracking technologies to create advertising profiles.

The App does not intentionally track users across unrelated websites.

Third-party websites linked from game threads may use their own cookies, analytics, or tracking technologies. Those practices are controlled by the respective third parties and are governed by their own privacy policies.

## 7. Information Sharing

We do not sell, rent, or otherwise commercially trade personal information collected through the App.

The App may interact with third-party services when necessary to provide its functionality.

These services include:

* **Reddit / Devvit**, which provides the platform on which the App operates.
* **ESPN**, which provides publicly available game information used by the scoreboard.
* Third-party websites linked in game threads, when a user chooses to follow an external link.

The App does not intentionally transmit Reddit user information to ESPN for advertising, profiling, or unrelated purposes.

## 8. Public Reddit Content

Content posted publicly on Reddit may be visible to the App when the App has permission to access it.

Game-thread posts created by the App are public Reddit posts and may therefore be viewed, indexed, copied, or otherwise processed by Reddit and other users in accordance with Reddit's policies.

The App does not claim ownership of content created by Reddit users.

Reddit users retain their rights in their user content subject to Reddit's applicable terms and policies.

## 9. Data Retention

The App retains application information only for as long as reasonably necessary to provide its functionality.

Application configuration stored in Redis may remain available until it is replaced or deleted by the App.

Reddit posts created by the App remain subject to Reddit's systems, retention practices, and policies.

The App does not maintain a separate long-term personal profile for individual Reddit users.

## 10. Automated Processing

Some App functions operate automatically through scheduled Devvit tasks.

The scheduled game-thread process may:

1. Retrieve current college hockey game information.
2. Generate scoreboard text.
3. Check recent Reddit posts for an existing game thread.
4. Determine whether an existing thread was created by the App.
5. Update an App-created game thread or create a new one.

Automated processing is limited to the functionality necessary to operate the game-thread and scoreboard features.

## 11. Data Security

We take reasonable measures to limit access to information used by the App.

However, no Internet transmission, online service, or storage system can be guaranteed to be completely secure.

The App relies on Reddit, Devvit, Redis, ESPN, and other third-party infrastructure, each of which maintains its own security practices.

## 12. Third-Party Services and Links

The App may provide links to external websites, including:

* Streaming services.
* Video services.
* College hockey organizations.
* Team websites.
* Conference websites.
* Community resources.

Following an external link takes you outside the App.

We are not responsible for the privacy practices, security, content, or data collection practices of third-party websites.

You should review the privacy policy of an external service before providing it with personal information.

## 13. Children's Privacy

The App is not specifically directed toward children and does not intentionally collect personal information from children.

The App operates within Reddit and is subject to Reddit's age requirements and policies.

## 14. Your Choices

You may stop interacting with the App at any time.

Where applicable, you may also remove the App from a subreddit or stop using features provided by the App.

Because the App operates within Reddit, some information associated with Reddit activity is controlled by Reddit rather than by the App developer.

Requests concerning Reddit account information should generally be directed to Reddit.

## 15. Changes to This Privacy Policy

We may update this Privacy Policy when the App's functionality, data practices, or applicable requirements change.

The **Last Updated** date at the top of this document will be updated when material changes are made.

You should periodically review this Privacy Policy for changes.

## 16. Contact

Questions about this Privacy Policy or ch-scorebot may be directed to the App developer through Reddit.

## 17. Relationship With Reddit

ch-scorebot is a third-party application built using Reddit's Developer Platform (Devvit).

The App is not Reddit itself and is not intended to replace Reddit's own privacy controls or policies.

Your use of Reddit remains subject to Reddit's applicable User Agreement, Privacy Policy, Developer Terms, and other Reddit policies.

---

**ch-scorebot**

**Last Updated: October 2, 2026**

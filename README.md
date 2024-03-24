# Code-Coverage-Trends

### Introduction
GitHub, as a hub of software collaboration and innovation, hosts countless repositories covering a wide array of projects. Understanding how the popularity of projects on GitHub correlates with their code quality is essential for advancing software development practices. In this study, we investigate this relationship by analyzing code coverage metrics within popular repositories over time. By uncovering patterns in code coverage progression, we aim to provide insights that can enhance testing practices, foster collaboration, and ultimately improve the quality of software delivered to users.

This project examines the link between the popularity of GitHub projects and their code quality, focusing on code coverage. It is a measure of how much of a project's code is tested, which can indicate its quality. We're interested in whether popular projects on GitHub also have high code coverage, and if improving code coverage can make a project more popular.

### Methodology

![Diagram](https://github.com/rajkunamaneni/Code-Coverage-Trends/blob/main/data/Pipeline%20of%20Method.png)

The research methodology encompasses a comprehensive analysis of GitHub repositories, employing statistical tools to examine the correlation between code coverage metrics and project popularity. We scrutinize code coverage trends over time, juxtaposed with the project's popularity indicators such as stars, forks, and pull requests. This approach enables us to identify patterns and deduce the influence of code coverage on a project's appeal within the GitHub community.

### Findings, Limitations, and Future Research

Results show a significant correlation between code coverage and project popularity, indicating that popular projects tend to have better code coverage. However, the link between high code coverage and high project popularity is weaker, suggesting other factors also influence a project's appeal. Introducing new features with substantial code coverage positively impacts project popularity.

While this study marks a significant stride in understanding the relationship between code coverage and project popularity, it acknowledges certain limitations, such as the reliance on pull requests as proxies for feature introductions. Acknowledging limitations such as using pull requests as a proxy for new feature introductions, we suggest future research directions including qualitative studies on developer perspectives and a broader analysis across different projects and platforms. While high code coverage correlates with increased project visibility on GitHub, other factors also influence popularity, highlighting the need for a comprehensive understanding of what drives project appeal.

### Repository Structure

This repository is organized as follows:

* ```src/```: Contains Python scripts designed for extracting data from GitHub and utilizing tools like CodeCov and CoverAll.
* ```data/```: Houses information about Popular Repositories.

You can find the CSV files that contain the raw data in the ```data/``` directory. In the CSV files, each row represents a repository snapshot. It gives a comprehensive view of code quality metrics and popularity indicators. Columns include Username, Repository, Percentage, Hash/commit identifier, Timestamp date, Language, Daily Star Count, Total Star, Additions, Deletions, Pull Requests on Timestamp, Contributions, and Total Pull Requests Before Timestamp. This format of the datasets was used for analyzing code quality and popularity trends on GitHub.

### Cloning the Repository

To replicate our analysis or obtain the data, you can clone this repository using the following commands:

```bash
git clone https://github.com/rajkunamaneni/Code-Coverage-Trends.git
cd src/
```

We invite you to explore our findings, contribute to the ongoing discussion, and perhaps extend the research to uncover further insights into the interplay between code quality and project popularity on GitHub.

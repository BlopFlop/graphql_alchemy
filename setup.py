from setuptools import setup


setup(
    name="graphql_alchemy",
    version="0.0.4",
    author="Artur Youngblood",
    author_email="arturungb@gmail.com",
    description="GraphQl query builder.",
    long_description=open("README.md").read(),
    packages=[
        "graphql_alchemy",
        "graphql_alchemy.converter",
        "graphql_alchemy.types",
    ],
    package_dir={
        "graphql_alchemy": "src",
        "graphql_alchemy.converter": "src/converter",
        "graphql_alchemy.types": "src/types",
    },
)

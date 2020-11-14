def coerce():
    """
    `coerce` is meant to do things.

    Examples:
        .. highlight:: python
        .. code-block:: python

            >>> from coercion import coerce

            >>> schema = {"foo": float, "bar": str}
            >>> record = {"foo": 1, "baz": 3.14}
            >>> coerce(schema, record)
            {'foo': 1.0, 'bar': None}

            # you can change the default type like:
            >>> coerce(schema, record, {str: ""})
            {'foo': 1.0, 'bar': ''}

            # what about lists behaving badly?
            >>> schema2 = {"foo": [float]}
            >>> record2 = {"foo": "[1, 2, 3]"}
            >>> coerce(schema2, record2)
            {'foo': [1.0, 2.0, 3.0]}

            # what about json strings?
            >>> schema3 = {"foo": {"bar": str}}
            >>> record3 = {"foo": '{"bar": 1}'}
            >>> coerce(schema3, record3)
            {'foo': {'bar': '1'}}

    Args:
        schema: A Python dict defining a schema
        record: A Python dict to coerce
        defaults: An optional dict mapping primitive types
            to their preferred default values

    Returns:
        A Python dict in the shape of `schema`
    """
    pass


def temp2():
    """testing again"""
    pass


def temp3():
    pass


def temp4():
    """
    Examples:
        .. highlight:: python
        .. code-block:: python

            >>> from json import dumps
            >>> print(dumps)
            <function dumps at 0x7f63d1725d30>
    """
    pass

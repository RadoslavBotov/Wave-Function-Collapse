from src.direction import Direction

# ==========================================================================

def test_invalid_value():
    # Arrange
    invalid = Direction.INVALID

    # Assert
    assert invalid == -1


def test_north_value():
    # Arrange
    north = Direction.NORTH

    # Assert
    assert north == 0


def test_east_value():
    # Arrange
    east = Direction.EAST

    # Assert
    assert east == 1


def test_south_value():
    # Arrange
    south = Direction.SOUTH

    # Assert
    assert south == 2


def test_west_value():
    # Arrange
    west = Direction.WEST

    # Assert
    assert west == 3

# ==========================================================================

def test_is_invalid_invalid():
    # Arrange
    invalid = Direction.INVALID

    # Assert
    assert invalid.is_invalid() == True


def test_is_invalid_north():
    # Arrange
    north = Direction.NORTH

    # Assert
    assert north.is_invalid() == False


def test_is_invalid_east():
    # Arrange
    east = Direction.EAST

    # Assert
    assert east.is_invalid() == False


def test_is_invalid_south():
    # Arrange
    south = Direction.SOUTH

    # Assert
    assert south.is_invalid() == False


def test_is_invalid_west():
    # Arrange
    west = Direction.WEST

    # Assert
    assert west.is_invalid() == False

# ==========================================================================

def test_get_opposite_invalid():
    # Arrange
    invalid = Direction.INVALID

    # Act
    opposite = invalid.get_opposite()

    # Assert
    assert opposite == Direction.INVALID


def test_get_opposite_north():
    # Arrange
    north = Direction.NORTH

    # Act
    opposite = north.get_opposite()

    # Assert
    assert opposite == Direction.SOUTH


def test_get_opposite_east():
    # Arrange
    east = Direction.EAST

    # Act
    opposite = east.get_opposite()

    # Assert
    assert opposite == Direction.WEST


def test_get_opposite_south():
    # Arrange
    south = Direction.SOUTH

    # Act
    opposite = south.get_opposite()

    # Assert
    assert opposite == Direction.NORTH


def test_get_opposite_west():
    # Arrange
    west = Direction.WEST

    # Act
    opposite = west.get_opposite()

    # Assert
    assert opposite == Direction.EAST

# ==========================================================================

def test_get_slice_north():
    # Arrange
    code = '123abc456def'
    west = Direction.NORTH

    # Act
    code_slice = code[west.get_slice()]

    # Assert
    assert code_slice == '123'


def test_get_slice_east():
    # Arrange
    code = '123abc456def'
    west = Direction.EAST

    # Act
    code_slice = code[west.get_slice()]

    # Assert
    assert code_slice == 'abc'


def test_get_slice_south():
    # Arrange
    code = '123abc456def'
    west = Direction.SOUTH

    # Act
    code_slice = code[west.get_slice()]

    # Assert
    assert code_slice == '456'


def test_get_slice_west():
    # Arrange
    code = '123abc456def'
    west = Direction.WEST

    # Act
    code_slice = code[west.get_slice()]

    # Assert
    assert code_slice == 'def'

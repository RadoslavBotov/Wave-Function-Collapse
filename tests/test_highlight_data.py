from src.highlight_data import HighlightData

# ==========================================================================

def test_default_values():
    # Arrange
    data = HighlightData()

    # Assert
    assert data.last_row == -1, 'last_row should be -1'
    assert data.last_column == -1, 'last_column should be -1'
    assert data.last_rect == None, 'last_rect should be -1'


# ==========================================================================

def test_update_none():
    # Arrange
    data = HighlightData(1, 2, 3)

    # Act
    data.update()

    # Assert
    assert data.last_row == 1, 'last_row should be 1'
    assert data.last_column == 2, 'last_column should be 2'
    assert data.last_rect == 3, 'last_rect should be 3'



def test_update_last_row_only():
    # Arrange
    data = HighlightData(1, 2, 3)

    # Act
    data.update(new_row=0)

    # Assert
    assert data.last_row == 0, 'last_row should be 1'
    assert data.last_column == 2, 'last_column should be 2'
    assert data.last_rect == 3, 'last_rect should be 3'



def test_update_none_last_column_only():
    # Arrange
    data = HighlightData(1, 2, 3)

    # Act
    data.update(new_column=0)

    # Assert
    assert data.last_row == 1, 'last_row should be 1'
    assert data.last_column == 0, 'last_column should be 0'
    assert data.last_rect == 3, 'last_rect should be 3'



def test_update_none_last_rect_only():
    # Arrange
    data = HighlightData(1, 2, 3)

    # Act
    data.update(new_last_rect=0)

    # Assert
    assert data.last_row == 1, 'last_row should be 1'
    assert data.last_column == 2, 'last_column should be 2'
    assert data.last_rect == 0, 'last_rect should be 0'


def test_update_all():
    # Arrange
    data = HighlightData(1, 2, 3)

    # Act
    data.update(10, 20, 30)

    # Assert
    assert data.last_row == 10, 'last_row should be 10'
    assert data.last_column == 20, 'last_column should be 20'
    assert data.last_rect == 30, 'last_rect should be 30'

# ==========================================================================

def test_check_match_false():
    # Arrange
    data = HighlightData(1, 2, 3)

    # Act
    result = data.check_match(0, 0)
    
    # Assert 
    assert result is False


def test_check_match_true():
    # Arrange
    data = HighlightData(1, 2, 3)

    # Act
    result = data.check_match(1, 2)
    
    # Assert 
    assert result is True


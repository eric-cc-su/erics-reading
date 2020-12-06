import React, { Component } from 'react';

class Book extends Component {
    /**
     * Book component to represent each book.
     */
    render() {
        let subtitle = null;
        if (this.props.subtitle) {
            subtitle = <h3 className="book-subtitle">{this.props.subtitle}</h3>;
        }
        return (
            <div className="book-container">
                <a href={this.props.bookUrl}>
                    <img className="book-cover-img"
                        src={this.props.bookImageUrl}
                        alt={this.props.title + " image"} />
                </a>
                <div className="book-title-text-container center-align">
                    <h2 className="book-title">{this.props.title}</h2>
                    {subtitle}
                    <h4 className="book-author">{this.props.author}</h4>
                </div>
            </div>
        )
    }
}

export default Book;
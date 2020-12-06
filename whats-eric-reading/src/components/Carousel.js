import React, { Component } from 'react';

class Carousel extends Component {
    /**
     * Book carousel component to show multiple Book components.
     */
    state = {
        books: []
    };

    componentDidMount() {
        console.log('Carousel component endpoint: ' + this.props.grEndpoint);
    };

    render() {
        return (
            <div className="books-carousel">
                <h2>This is the carousel</h2>
            </div>
        )
    };
};

export default Carousel;
// withFetchHOC.js
import React, { Component } from "react";

/**
 * A higher-order component that fetches data when the wrapped component mounts.
 *
 * @param {React.Component} WrappedComponent - The component to wrap.
 * @param {Function} fetchFunction - The function to fetch data.
 * @param {string} newElementLink - The link for creating new elements.
 * @return {React.Component} The wrapped component.
 */
const withFetchHOC = (WrappedComponent, fetchFunction, newElementLink) => {
  return class withFetch extends Component {
    state = {
      data: [],
      loading: true,
      error: null,
    };

    /**
     * Fetches data when the component mounts.
     */
    async componentDidMount() {
      try {
        const data = await fetchFunction();
        this.setState({ data, loading: false });
      } catch (error) {
        this.setState({ error, loading: false });
      }
    }

    /**
     * Renders the wrapped component with the fetched data, or a loading message, or an error message.
     *
     * @return {React.Element} The rendered element.
     */
    render() {
      const { loading, data, error } = this.state;

      if (loading) {
        return <div>Loading...</div>;
      }

      if (error) {
        return <div>Error: {error.message}</div>;
      }

      return (
        <WrappedComponent
          data={data}
          newElementLink={newElementLink}
          {...this.props}
        />
      );
    }
  };
};

export default withFetchHOC;

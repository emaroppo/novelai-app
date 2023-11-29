// withFetchHOC.js
import React, { Component } from 'react';

const withFetchHOC = (WrappedComponent, fetchFunction, newElementLink) => {
  return class extends Component {
    state = {
      data: [],
      loading: true,
      error: null
    };

    async componentDidMount() {
      try {
        const data = await fetchFunction();
        this.setState({ data, loading: false });
      } catch (error) {
        this.setState({ error, loading: false });
      }
    }

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
